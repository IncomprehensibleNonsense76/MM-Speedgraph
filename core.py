"""Core types for the MM-Speedgraph routing engine.

Technique: atomic trick/movement (bomb boost, superslide, backwalk, etc.)
Strat: composed sequence of techniques applied to a traversal
Ruleset: category hierarchy that filters available strats
Node: location in the game world with checks and properties
GameGraph: unified graph of nodes, edges (with strats), and checks
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import IntEnum
from collections import defaultdict
import heapq


# =============================================================================
# Rulesets
# =============================================================================


class Ruleset(IntEnum):
    """Speedrun category rulesets, ordered from most restrictive to least.
    Each level includes all strats from levels below it."""

    GLITCHLESS = 0
    BUGLIMIT = 1
    RESTRICTED = 2  # ADR only — no equipswap or index warp
    NMG = 3
    RMG = 4  # SRM allowed, no ACE/text overflow
    UNRESTRICTED = 5  # anything goes


class Version(IntEnum):
    """Game versions. Lower = more restrictive strat compatibility."""

    JP_1_0 = 0
    JP_1_1 = 1
    EN = 2

    @classmethod
    def all(cls) -> frozenset[Version]:
        return frozenset(cls)


class Platform(IntEnum):
    """Hardware platforms. Some glitches are platform-specific."""

    N64 = 0
    GCN = 1
    WII_VC = 2
    WII_U_VC = 3
    SWITCH = 4  # includes switch 2
    # PAL exists but runs at 17 FPS — not viable for speedrunning

    @classmethod
    def all(cls) -> frozenset[Platform]:
        return frozenset(cls)


# =============================================================================
# Techniques
# =============================================================================


@dataclass(frozen=True)
class Technique:
    """An atomic trick or movement option.

    Techniques are the building blocks of strats. They declare what items
    are required, what resources are consumed, and what ruleset allows them.

    Examples:
        backwalk = Technique("Backwalk")
        isg = Technique("ISG", consumes={"bombs": 1}, ruleset=Ruleset.NMG)
        bomb_boost = Technique("Bomb Boost", consumes={"bombs": 1})
    """

    name: str
    requires: frozenset[str] = frozenset()
    consumes: dict[str, int] = field(default_factory=dict)
    ruleset: Ruleset = Ruleset.GLITCHLESS

    def __hash__(self):
        return hash(self.name)


# =============================================================================
# Strats
# =============================================================================


@dataclass
class Strat:
    """A traversal strategy composed of techniques.

    Applied to edges in the graph. The solver picks the cheapest strat
    whose requirements are met and whose ruleset is allowed.

    Cost is in seconds. Requirements and consumption are auto-computed
    from techniques unless explicitly overridden.

    Examples:
        Strat("Backwalk", cost=45)
        Strat("Torch Mega", cost=25, techniques=[isg, hover, mega_flip])
        Strat("Hookshot", cost=10, requires=frozenset({I.Hookshot}))
    """

    name: str
    cost: int
    techniques: list[Technique] = field(default_factory=list)
    requires: frozenset[str] | None = None
    consumes: dict[str, int] | None = None
    ruleset: Ruleset | None = None
    oneway: bool = False
    versions: frozenset[Version] | None = None  # None = all versions
    platforms: frozenset[Platform] | None = None  # None = all platforms

    @property
    def total_requires(self) -> frozenset[str]:
        if self.requires is not None:
            return self.requires
        return frozenset().union(*(t.requires for t in self.techniques))

    @property
    def total_consumes(self) -> dict[str, int]:
        if self.consumes is not None:
            return self.consumes
        result: dict[str, int] = {}
        for t in self.techniques:
            for item, count in t.consumes.items():
                result[item] = result.get(item, 0) + count
        return result

    @property
    def min_ruleset(self) -> Ruleset:
        if self.ruleset is not None:
            return self.ruleset
        if not self.techniques:
            return Ruleset.GLITCHLESS
        return max(t.ruleset for t in self.techniques)


# =============================================================================
# Checks (items acquirable at nodes)
# =============================================================================


@dataclass
class Check:
    """An item, song, mask, or event acquirable at a node."""

    id: str
    requires: frozenset[str] = frozenset()
    time: frozenset[int] | None = None  # TimeSlot values, None = any time
    duration: int = 0
    warp_to: str | None = None

    @property
    def label(self) -> str:
        return self.id.label if hasattr(self.id, "label") else str(self.id)


# =============================================================================
# Nodes
# =============================================================================


@dataclass
class Node:
    """A location in the game world (scene, room, or cell position)."""

    id: str
    checks: list[Check] = field(default_factory=list)
    owl_statue: bool = False
    actors: set[str] = field(default_factory=set)  # enemies, objects, etc.

    def check(
        self,
        item_id: str,
        requires: set[str] | None = None,
        time: frozenset[int] | None = None,
        duration: int = 0,
        warp_to: str | None = None,
    ) -> Node:
        """Add a check (acquirable item) to this node. Returns self for chaining."""
        self.checks.append(
            Check(
                id=item_id,
                requires=frozenset(requires) if requires else frozenset(),
                time=time,
                duration=duration,
                warp_to=warp_to,
            )
        )
        return self


# =============================================================================
# GameGraph
# =============================================================================


class GameGraph:
    """Unified graph of game locations, traversals, and acquirable items.

    Nodes are locations (scenes, rooms, cell positions).
    Edges are connections with one or more strats.
    Checks are items/events at nodes.

    The solver filters strats by the active ruleset, then uses Dijkstra
    to find the cheapest route through the graph.
    """

    def __init__(
        self,
        ruleset: Ruleset = Ruleset.GLITCHLESS,
        version: Version = Version.EN,
        platform: Platform = Platform.N64,
    ):
        self.ruleset = ruleset
        self.version = version
        self.platform = platform
        self._nodes: dict[str, Node] = {}
        self._edges: dict[str, dict[str, list[Strat]]] = defaultdict(
            lambda: defaultdict(list)
        )

    # --- Building the graph ---

    def node(self, id: str, **kwargs) -> Node:
        """Get or create a node."""
        if id not in self._nodes:
            self._nodes[id] = Node(id=id, **kwargs)
        return self._nodes[id]

    def connect(self, a: str, b: str, strat: Strat) -> GameGraph:
        """Add a strat to the edge from a to b. Returns self for chaining."""
        self.node(a)
        self.node(b)
        self._edges[a][b].append(strat)
        if not strat.oneway:
            self._edges[b][a].append(strat)
        return self

    # --- Querying the graph ---

    @property
    def nodes(self) -> dict[str, Node]:
        return self._nodes

    def strats_for(self, a: str, b: str) -> list[Strat]:
        """All strats on the edge from a to b (unfiltered)."""
        return self._edges.get(a, {}).get(b, [])

    def _strat_allowed(self, strat: Strat) -> bool:
        """Check if a strat is allowed by current ruleset, version, and platform."""
        if strat.min_ruleset > self.ruleset:
            return False
        if strat.versions and self.version not in strat.versions:
            return False
        if strat.platforms and self.platform not in strat.platforms:
            return False
        return True

    def available_strats(
        self, a: str, b: str, acquired: frozenset[str] | None = None
    ) -> list[Strat]:
        """Strats on edge a->b that are allowed and whose requirements are met."""
        result = []
        for s in self.strats_for(a, b):
            if not self._strat_allowed(s):
                continue
            if s.total_requires and (
                acquired is None or not s.total_requires <= acquired
            ):
                continue
            result.append(s)
        return result

    def best_strat(
        self, a: str, b: str, acquired: frozenset[str] | None = None
    ) -> Strat | None:
        """Cheapest available strat on edge a->b, or None."""
        strats = self.available_strats(a, b, acquired)
        return min(strats, key=lambda s: s.cost) if strats else None

    # --- Pathfinding ---

    def dijkstra(
        self, start: str, acquired: frozenset[str] | None = None
    ) -> dict[str, int]:
        """Shortest path distances from start, respecting ruleset/version/platform and requirements."""
        dist = {start: 0}
        heap = [(0, start)]
        while heap:
            d, node = heapq.heappop(heap)
            if d > dist.get(node, float("inf")):
                continue
            for neighbor, strats in self._edges.get(node, {}).items():
                for s in strats:
                    if not self._strat_allowed(s):
                        continue
                    if s.total_requires and (
                        acquired is None or not s.total_requires <= acquired
                    ):
                        continue
                    nd = d + s.cost
                    if nd < dist.get(neighbor, float("inf")):
                        dist[neighbor] = nd
                        heapq.heappush(heap, (nd, neighbor))
        return dist

    def path(
        self, start: str, end: str, acquired: frozenset[str] | None = None
    ) -> list[str] | None:
        """Shortest path from start to end."""
        if start == end:
            return [start]
        dist = {start: 0}
        prev: dict[str, str | None] = {start: None}
        heap = [(0, start)]
        while heap:
            d, node = heapq.heappop(heap)
            if node == end:
                result = []
                cur: str | None = end
                while cur is not None:
                    result.append(cur)
                    cur = prev[cur]
                return list(reversed(result))
            if d > dist.get(node, float("inf")):
                continue
            for neighbor, strats in self._edges.get(node, {}).items():
                for s in strats:
                    if not self._strat_allowed(s):
                        continue
                    if s.total_requires and (
                        acquired is None or not s.total_requires <= acquired
                    ):
                        continue
                    nd = d + s.cost
                    if nd < dist.get(neighbor, float("inf")):
                        dist[neighbor] = nd
                        prev[neighbor] = node
                        heapq.heappush(heap, (nd, neighbor))
        return None

    # --- Checks ---

    def all_checks(self) -> dict[str, tuple[Check, str]]:
        """All checks in the graph as {check_id: (Check, node_id)}."""
        result = {}
        for node_id, node in self._nodes.items():
            for check in node.checks:
                result[check.id] = (check, node_id)
        return result

    # --- Stats ---

    def stats(self) -> str:
        n_nodes = len(self._nodes)
        n_edges = sum(len(neighbors) for neighbors in self._edges.values())
        n_strats = sum(
            len(strats)
            for neighbors in self._edges.values()
            for strats in neighbors.values()
        )
        n_checks = sum(len(n.checks) for n in self._nodes.values())
        n_owls = sum(1 for n in self._nodes.values() if n.owl_statue)
        visible = sum(
            1
            for neighbors in self._edges.values()
            for strats in neighbors.values()
            for s in strats
            if s.min_ruleset <= self.ruleset
        )
        return (
            f"{n_nodes} nodes | {n_edges} edges | {n_strats} strats "
            f"({visible} visible at {self.ruleset.name}) | {n_checks} checks | {n_owls} owls"
        )
