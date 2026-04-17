"""Route solver that operates on GameGraph.

Greedy nearest-available with cycle awareness, SOS warps,
owl activation tracking, and automatic SOS A/B testing.
"""

from __future__ import annotations
from collections import deque
from core import GameGraph, Check, Strat, Ruleset
from enums import Scene, Masks, Songs, TimeSlot
from world import SOS_COST


def _find_needed(
    checks: dict[str, tuple[Check, str]],
    goals: list[str],
) -> set[str]:
    """Transitive closure of all check IDs required to achieve goals."""
    needed: set[str] = set()
    queue = deque(goals)
    while queue:
        cid = queue.popleft()
        if cid in needed:
            continue
        if cid not in checks:
            raise KeyError(f"Unknown check: {cid!r}")
        needed.add(cid)
        check, _ = checks[cid]
        for req in check.requires:
            queue.append(req)
    return needed


def _parent_scene(node: str) -> str:
    return node.rsplit(":", 1)[0] if ":" in node else node


# Map dungeon scenes to their entry room nodes
DUNGEON_ENTRIES: dict[str, str] = {}


def _register_dungeon_entry(scene: str, entry_room: str):
    """Register a dungeon's entry room for SOS-to-entrance behavior."""
    DUNGEON_ENTRIES[scene] = entry_room


def _best_sos(
    current: str,
    dest: str,
    has_sos: bool,
    activated_owls: set[str],
    graph: GameGraph,
    acquired_frozen: frozenset[str],
) -> tuple[float, str | None]:
    """Cheapest SOS warp to reach dest.

    SOS behavior:
    - In overworld: warp to any activated owl statue
    - In dungeon room: warp to dungeon entrance (then can exit to overworld)
    """
    best_cost: float = float("inf")
    best_owl = None

    # Standard owl warps
    for owl in activated_owls:
        walk = graph.dijkstra(owl, acquired_frozen).get(dest, float("inf"))
        total = SOS_COST + walk
        if total < best_cost:
            best_cost = total
            best_owl = owl

    # Dungeon entrance warp: if currently in a dungeon room, SOS goes to entrance
    if ":" in current:
        parent = _parent_scene(current)
        entry = DUNGEON_ENTRIES.get(parent)
        if entry and entry != current:
            walk = graph.dijkstra(entry, acquired_frozen).get(dest, float("inf"))
            total = SOS_COST + walk
            if total < best_cost:
                best_cost = total
                best_owl = entry

    return best_cost, best_owl


def _travel(
    current: str,
    dest: str,
    has_sos: bool,
    activated_owls: set[str],
    graph: GameGraph,
    acquired_frozen: frozenset[str],
) -> tuple[float, list[str], str]:
    """Best travel option (walk or SOS). Returns (cost, path, method)."""
    if current == dest:
        return 0, [current], "stay"

    walk_cost = graph.dijkstra(current, acquired_frozen).get(dest, float("inf"))
    walk_path = graph.path(current, dest, acquired_frozen) or [current]
    best_cost, best_path, method = walk_cost, walk_path, "walk"

    if has_sos and (activated_owls or ":" in current):
        sos_cost, sos_owl = _best_sos(current, dest, has_sos, activated_owls, graph, acquired_frozen)
        if sos_cost < best_cost:
            walk_seg = graph.path(sos_owl, dest, acquired_frozen)
            if walk_seg and len(walk_seg) > 1:
                best_path = ["~SOS~"] + walk_seg
            else:
                best_path = ["~SOS~", dest]
            best_cost = sos_cost
            method = "sos"

    return best_cost, best_path, method


# =============================================================================
# Cycle route
# =============================================================================

class CycleRoute:
    def __init__(self, cycle_num: int):
        self.cycle_num = cycle_num
        self.steps: list[tuple[Check, str, float, list[str]]] = []  # (check, node_id, cost, path)
        self.total_cost: float = 0

    def add(self, check: Check, node_id: str, cost: float, path: list[str]):
        self.steps.append((check, node_id, cost, path))
        self.total_cost += cost


def _total_cost(cycles: list[CycleRoute]) -> float:
    return sum(c.total_cost for c in cycles)


# =============================================================================
# Main solver
# =============================================================================

def solve(
    graph: GameGraph,
    goals: list[str],
) -> list[CycleRoute]:
    """Solve with automatic SOS A/B test."""
    all_checks = graph.all_checks()
    needed = _find_needed(all_checks, goals)

    # Try both with and without SOS, pick the cheaper one that works
    routes: list[list[CycleRoute]] = []

    for try_sos in [False, True]:
        if try_sos and Songs.Soaring in needed:
            continue  # SOS already required, skip duplicate
        if try_sos and Songs.Soaring not in all_checks:
            continue  # SOS not available

        try_goals = list(goals) + ([Songs.Soaring] if try_sos else [])
        try:
            result = _solve(graph, try_goals, all_checks)
            routes.append(result)
        except ValueError:
            continue  # this variant got stuck, try the other

    if not routes:
        raise ValueError("No valid route found for any SOS configuration")

    return min(routes, key=_total_cost)


def _solve(
    graph: GameGraph,
    goals: list[str],
    all_checks: dict[str, tuple[Check, str]],
) -> list[CycleRoute]:
    needed = _find_needed(all_checks, goals)

    acquired: set[str] = set()
    activated_owls: set[str] = set()
    has_sos = False
    can_activate = False  # need Deku Mask (human + sword) to hit owl statues
    cycles: list[CycleRoute] = []

    # Collect owl statue nodes
    owl_nodes = {node_id for node_id, node in graph.nodes.items() if node.owl_statue}

    while acquired != needed:
        cycle = CycleRoute(len(cycles) + 1)
        current = Scene.ClockTowerInterior
        current_time = TimeSlot.DAY_1

        made_progress = True
        while made_progress:
            made_progress = False
            acquired_frozen = frozenset(acquired)

            # Find checks available right now (deps met + time valid)
            available = []
            for cid in needed:
                if cid in acquired:
                    continue
                check, node_id = all_checks[cid]
                if not check.requires <= acquired:
                    continue
                if check.time is None:
                    available.append(cid)
                elif any(t >= current_time for t in check.time):
                    available.append(cid)

            if not available:
                break

            # Cache dijkstra from current position
            dist_from_current = graph.dijkstra(current, acquired_frozen)

            # Filter to physically reachable (walk, SOS owl, or SOS dungeon entrance)
            reachable = []
            can_sos = has_sos and (activated_owls or ":" in current)
            for cid in available:
                _, node_id = all_checks[cid]
                cost = dist_from_current.get(node_id, float("inf"))
                if can_sos:
                    sos_cost, _ = _best_sos(current, node_id, has_sos, activated_owls, graph, acquired_frozen)
                    cost = min(cost, sos_cost)
                if cost < float("inf"):
                    reachable.append(cid)
            available = reachable

            if not available:
                # No reachable checks right now — try advancing time
                future = []
                for cid in needed:
                    if cid in acquired:
                        continue
                    check, node_id = all_checks[cid]
                    if not check.requires <= acquired:
                        continue
                    if check.time and all(t < current_time for t in check.time):
                        continue  # already past this time slot
                    if check.time and any(t > current_time for t in check.time):
                        future.append(min(t for t in check.time if t > current_time))
                if future:
                    current_time = min(future)
                    continue  # retry with advanced time
                break

            # Score: prefer current time slot, then nearest
            def score(cid):
                check, node_id = all_checks[cid]
                travel = dist_from_current.get(node_id, float("inf"))
                if can_sos:
                    sos_cost, _ = _best_sos(current, node_id, has_sos, activated_owls, graph, acquired_frozen)
                    travel = min(travel, sos_cost)

                time_wait = 0
                if check.time is not None:
                    earliest = min(t for t in check.time if t >= current_time)
                    time_wait = earliest - current_time

                return (time_wait, travel + check.duration)

            best_id = min(available, key=score)
            best_check, best_node = all_checks[best_id]

            # Advance time if needed
            if best_check.time is not None:
                earliest_valid = min(t for t in best_check.time if t >= current_time)
                current_time = earliest_valid

            # Travel
            travel_cost, path, _ = _travel(
                current, best_node, has_sos, activated_owls, graph, acquired_frozen)
            total_cost = travel_cost + best_check.duration

            cycle.add(best_check, best_node, total_cost, path)

            # Update position
            current = best_check.warp_to if best_check.warp_to else best_node
            acquired.add(best_id)
            made_progress = True

            # Track SOS / owl state
            if best_id == Songs.Soaring:
                has_sos = True
            if best_id == Masks.Deku:
                can_activate = True
            if can_activate:
                for scene in path:
                    ps = _parent_scene(scene)
                    if ps in owl_nodes:
                        activated_owls.add(ps)
                if best_check.warp_to:
                    ps = _parent_scene(best_check.warp_to)
                    if ps in owl_nodes:
                        activated_owls.add(ps)

        cycles.append(cycle)

        if not cycle.steps:
            missing = needed - acquired
            raise ValueError(f"Stuck! No checks possible. Missing: {missing}")

    return cycles


# =============================================================================
# Display
# =============================================================================

TIME_NAMES = {
    TimeSlot.DAY_1: "Day 1", TimeSlot.NIGHT_1: "Night 1",
    TimeSlot.DAY_2: "Day 2", TimeSlot.NIGHT_2: "Night 2",
    TimeSlot.DAY_3: "Day 3", TimeSlot.NIGHT_3: "Night 3",
}


def fmt_time(seconds: float) -> str:
    s = int(seconds)
    if s < 60:
        return f"{s}s"
    m, s = divmod(s, 60)
    if s == 0:
        return f"{m}m"
    return f"{m}m {s}s"


def print_route(goal_name: str, cycles: list[CycleRoute], graph: GameGraph):
    print(f"=== {goal_name} ({graph.ruleset.name}, {graph.version.name}, {graph.platform.name}) ===")

    total_time: float = 0
    total_checks = 0
    total_sos = 0

    for cycle in cycles:
        print(f"\n{'─' * 60}")
        print(f"  CYCLE {cycle.cycle_num} (start: Clock Tower Interior, Day 1)")
        print(f"{'─' * 60}")

        current_scene = Scene.ClockTowerInterior
        step = 0
        last_time = None

        for check, node_id, cost, path in cycle.steps:
            # Time slot header
            if check.time is not None:
                earliest = min(check.time)
                if last_time is None or earliest > last_time:
                    last_time = earliest
                    print(f"\n  --- {TIME_NAMES[earliest]} ---")

            if node_id != current_scene:
                step += 1
                is_sos = len(path) > 0 and path[0] == "~SOS~"
                if is_sos:
                    total_sos += 1
                travel = " -> ".join(path)
                print(f"\n  [{step}] {travel}  ({fmt_time(cost)})")
                current_scene = check.warp_to or node_id
            else:
                if step == 0:
                    step += 1
                    print(f"\n  [{step}] {node_id}  (start)")
                elif cost > 0:
                    print(f"       (+{fmt_time(cost)})")
                current_scene = check.warp_to or node_id
            print(f"       >> {check.label}")

            if check.warp_to and check.warp_to != node_id:
                print(f"       ~~ warp to {check.warp_to}")

        total_time += cycle.total_cost
        total_checks += len(cycle.steps)

        if cycle.cycle_num < len(cycles):
            print(f"\n  >> Song of Time -> Clock Tower Interior, Day 1")

    print(f"\n{'=' * 60}")
    print(f"  {total_checks} checks | {len(cycles)} cycles | "
          f"{fmt_time(total_time)} ({int(total_time)}s) | {total_sos} SOS")
