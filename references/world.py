from __future__ import annotations
import heapq
from collections import defaultdict
from enums import Scene as S, Items as I, Masks as M, Songs


DEFAULT_WEIGHT = 30  # seconds per scene transition
TF_WEIGHT = 45  # Termina Field crossings
SOS_COST = 15  # Song of Soaring warp

# Edge format:
#   (a, b)              — bidirectional, default weight, no requirements
#   (a, b, int)         — bidirectional, explicit weight, no requirements
#   (a, b, strats)      — bidirectional, list of (cost, requires) strats
#
# Solver picks cheapest strat whose requirements are met.

EDGES = [
    # === Clock Town internal (all free) ===
    (S.SouthClockTown, S.NorthClockTown),
    (S.SouthClockTown, S.EastClockTown),
    (S.SouthClockTown, S.WestClockTown),
    (S.SouthClockTown, S.LaundryPool),
    (S.SouthClockTown, S.ClockTowerInterior),
    (S.NorthClockTown, S.EastClockTown),
    (S.NorthClockTown, S.CTGreatFairyFountain),
    (S.ClockTowerInterior, S.ClockTowerRooftop),
    (S.EastClockTown, S.Observatory),
    # === Clock Town <-> Overworld ===
    (S.SouthClockTown, S.TerminaField),
    # === Termina Field exits ===
    (S.TerminaField, S.SouthernSwamp, 180),  # 3 min cutscene
    (S.TerminaField, S.PathToMountainVillage),  # free (ice/boulders gate is deeper in)
    (
        S.TerminaField,
        S.GreatBayCoast,
        [(TF_WEIGHT, {I.Epona}), (TF_WEIGHT, {M.Goron, I.BombBag})],
    ),  # fence: Epona or Goron+Bombs
    (S.TerminaField, S.MilkRoad),  # free
    (S.TerminaField, S.IkanaTrail),  # free
    # === Southern Swamp area ===
    (S.SouthernSwamp, S.DekuPalace),
    (S.SouthernSwamp, S.Woodfall),
    (S.SouthernSwamp, S.WoodsOfMystery),
    (S.SouthernSwamp, S.HagsPotionShop),
    (S.SouthernSwamp, S.SwampSpiderHouse),
    # NOTE: Woodfall -> WFT edge handled by dungeon room expansion
    (S.DekuPrincessPrison, S.Woodfall),
    # === Mountain / Snowhead ===
    (
        S.PathToMountainVillage,
        S.MountainVillage,
        [(30, {I.Bow, I.BombBag})],
    ),  # ice (bow) + boulders (bombs)
    (S.MountainVillage, S.PathToGoronVillage),
    (S.MountainVillage, S.PathToSnowhead),
    (S.PathToGoronVillage, S.GoronVillage),
    (S.PathToGoronVillage, S.GoronRacetrack),
    (S.GoronVillage, S.GoronShrine),
    (S.GoronVillage, S.LonePeakShrine),
    (S.PathToSnowhead, S.Snowhead),
    (
        S.Snowhead,
        S.SnowheadTemple,
        [(30, {M.Goron, Songs.Lullaby})],
    ),  # Goron Lullaby to open entrance
    # === Milk Road / Ranch ===
    (S.MilkRoad, S.RomaniRanch, [(30, {I.PowderKeg})]),  # Powder Keg to blow boulder
    (S.MilkRoad, S.GormanTrack),
    # === Great Bay ===
    (S.GreatBayCoast, S.PiratesFortress, [(30, {M.Zora})]),  # swim as Zora
    (S.GreatBayCoast, S.MarineResearchLab),
    (S.GreatBayCoast, S.ZoraCape),
    (
        S.ZoraCape,
        S.GreatBayTemple,
        [(30, {Songs.NewWave})],
    ),  # turtle ride from New Wave
    # === Great Bay (other) ===
    (S.GreatBayCoast, S.PinnacleRock),
    (S.GreatBayCoast, S.OceanSpiderHouse),
    # === Ikana ===
    (
        S.IkanaTrail,
        S.IkanaGraveyard,
        [(30, {I.Epona}), (30, {M.Goron, I.BombBag})],
    ),  # before Garo gate
    (
        S.IkanaTrail,
        S.IkanaCanyon,
        [
            (30, {M.Garo, I.Hookshot, I.Epona}),  # full gate: Garo + Hookshot + access
            (30, {M.Garo, I.Hookshot, M.Goron, I.BombBag}),
        ],
    ),
    (S.IkanaCanyon, S.IkanaGraveyard),  # free once in canyon
    (S.IkanaCanyon, S.BeneathTheWell),
    (S.BeneathTheWell, S.IkanaCastle),
    (S.IkanaCanyon, S.StoneTower),
    (
        S.StoneTower,
        S.StoneTowerTemple,
        [(30, {Songs.Elegy, M.Goron, M.Zora, M.Deku})],
    ),  # Elegy statues + all forms
    # === Special ===
    (S.ClockTowerRooftop, S.TheMoon, 600),
]


# Scenes that have owl statues
OWL_SCENES = {
    S.SouthClockTown,
    S.SouthernSwamp,
    S.Woodfall,
    S.MountainVillage,
    S.Snowhead,
    S.MilkRoad,
    S.GreatBayCoast,
    S.ZoraCape,
    S.IkanaCanyon,
    S.StoneTower,
}


def _edge_weight(a, b, explicit=None):
    if explicit is not None:
        return explicit
    if a == S.TerminaField or b == S.TerminaField:
        return TF_WEIGHT
    return DEFAULT_WEIGHT


class World:
    def __init__(self, edges=None, dungeons=None):
        if edges is None:
            edges = EDGES
        self.adj: dict[str, dict[str, list[tuple[int, frozenset | None]]]] = (
            defaultdict(lambda: defaultdict(list))
        )

        # Add scene-level edges
        for edge in edges:
            a, b = edge[0], edge[1]
            rest = edge[2] if len(edge) > 2 else None

            if rest is None:
                # Default weight, no requirements
                w = _edge_weight(a, b)
                self.adj[a][b].append((w, None))
                self.adj[b][a].append((w, None))
            elif isinstance(rest, int):
                # Explicit weight, no requirements
                self.adj[a][b].append((rest, None))
                self.adj[b][a].append((rest, None))
            elif isinstance(rest, list):
                # Multiple strats: [(cost, requires), ...]
                for cost, req in rest:
                    req_frozen = frozenset(req) if req else None
                    self.adj[a][b].append((cost, req_frozen))
                    self.adj[b][a].append((cost, req_frozen))

        # Expand dungeon room graphs
        if dungeons is None:
            from dungeons import ALL_DUNGEONS, expand_dungeon

            dungeons = ALL_DUNGEONS
        for dungeon in dungeons:
            from dungeons import expand_dungeon

            room_edges, entry_node = expand_dungeon(dungeon)
            for edge in room_edges:
                a, b, w, req = edge
                req_frozen = frozenset(req) if req else None
                self.adj[a][b].append((w, req_frozen))

        self.nodes = set(self.adj.keys())

    def dijkstra(
        self, start: str, acquired: frozenset[str] | None = None
    ) -> dict[str, int]:
        """Shortest path distances from start, respecting edge requirements."""
        dist = {start: 0}
        heap = [(0, start)]
        while heap:
            d, node = heapq.heappop(heap)
            if d > dist.get(node, float("inf")):
                continue
            for neighbor, edge_options in self.adj[node].items():
                for weight, req in edge_options:
                    if req and (acquired is None or not req <= acquired):
                        continue
                    nd = d + weight
                    if nd < dist.get(neighbor, float("inf")):
                        dist[neighbor] = nd
                        heapq.heappush(heap, (nd, neighbor))
        return dist

    def distance(
        self, a: str, b: str, acquired: frozenset[str] | None = None
    ) -> int | None:
        if a == b:
            return 0
        return self.dijkstra(a, acquired).get(b)

    def path(
        self, start: str, end: str, acquired: frozenset[str] | None = None
    ) -> list[str] | None:
        """Shortest weighted path respecting requirements."""
        if start == end:
            return [start]
        dist = {start: 0}
        prev = {start: None}
        heap = [(0, start)]
        while heap:
            d, node = heapq.heappop(heap)
            if node == end:
                result = []
                cur = end
                while cur is not None:
                    result.append(cur)
                    cur = prev[cur]
                return list(reversed(result))
            if d > dist.get(node, float("inf")):
                continue
            for neighbor, edge_options in self.adj[node].items():
                for weight, req in edge_options:
                    if req and (acquired is None or not req <= acquired):
                        continue
                    nd = d + weight
                    if nd < dist.get(neighbor, float("inf")):
                        dist[neighbor] = nd
                        prev[neighbor] = node
                        heapq.heappush(heap, (nd, neighbor))
        return None
