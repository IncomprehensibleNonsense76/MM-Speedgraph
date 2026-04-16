from collections import deque
from model import Check
from enums import Scene as S, Masks as M, Songs, TimeSlot as T
from world import World, OWL_SCENES, SOS_COST


def _find_needed(checks: dict[str, Check], goals: list[str]) -> set[str]:
    """Transitive closure — all check IDs required to achieve goals."""
    needed: set[str] = set()
    queue = deque(goals)
    while queue:
        cid = queue.popleft()
        if cid in needed:
            continue
        if cid not in checks:
            raise KeyError(f"Unknown check: {cid!r}")
        needed.add(cid)
        for req in checks[cid].requires:
            queue.append(req)
    return needed


def _best_sos(
    current: str, dest: str, activated_owls: set[str],
    world: World, acquired_frozen: frozenset[str],
) -> tuple[int, str | None]:
    """Find cheapest SOS warp to reach dest. Returns (cost_seconds, owl_scene)."""
    best_cost = float("inf")
    best_owl = None
    for owl in activated_owls:
        walk_from_owl = world.dijkstra(owl, acquired_frozen).get(dest, float("inf"))
        total = SOS_COST + walk_from_owl
        if total < best_cost:
            best_cost = total
            best_owl = owl
    return best_cost, best_owl


def _travel(current, dest, has_sos, activated_owls, world, acquired_frozen):
    """Best travel option (walk or SOS). Returns (cost_seconds, path, method)."""
    if current == dest:
        return 0, [current], "stay"

    walk_cost = world.dijkstra(current, acquired_frozen).get(dest, float("inf"))
    walk_path = world.path(current, dest, acquired_frozen) or [current]
    best_cost, best_path, method = walk_cost, walk_path, "walk"

    if has_sos and activated_owls:
        sos_cost, sos_owl = _best_sos(current, dest, activated_owls, world, acquired_frozen)
        if sos_cost < best_cost:
            walk_seg = world.path(sos_owl, dest, acquired_frozen)
            if walk_seg and len(walk_seg) > 1:
                best_path = ["~SOS~"] + walk_seg
            else:
                best_path = ["~SOS~", dest]
            best_cost = sos_cost
            method = "sos"

    return best_cost, best_path, method


def _fmt_time(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    m, s = divmod(seconds, 60)
    if s == 0:
        return f"{m}m"
    return f"{m}m {s}s"


def _parent_scene(node: str) -> str:
    """Extract parent scene from a room node like 'Woodfall Temple:Room5'."""
    return node.rsplit(":", 1)[0] if ":" in node else node


# =============================================================================
# Cycle-aware solver
# =============================================================================

class CycleRoute:
    def __init__(self, cycle_num):
        self.cycle_num = cycle_num
        self.steps: list[tuple[Check, int, list[str]]] = []
        self.total_cost = 0

    def add(self, check, cost, path):
        self.steps.append((check, cost, path))
        self.total_cost += cost


def _total_cost(cycles: list[CycleRoute]) -> int:
    return sum(c.total_cost for c in cycles)


def solve_route_cycles(
    checks: dict[str, Check],
    goals: list[str],
    world: World,
) -> list[CycleRoute]:
    """Greedy solver with automatic A/B test for Song of Soaring."""
    route_a = _solve_route_cycles(checks, goals, world)
    if Songs.Soaring not in _find_needed(checks, goals):
        goals_with_sos = list(goals) + [Songs.Soaring]
        route_b = _solve_route_cycles(checks, goals_with_sos, world)
        if _total_cost(route_b) < _total_cost(route_a):
            return route_b
    return route_a


def _solve_route_cycles(
    checks: dict[str, Check],
    goals: list[str],
    world: World,
) -> list[CycleRoute]:
    needed = _find_needed(checks, goals)

    acquired: set[str] = set()
    activated_owls: set[str] = set()
    has_sos = False
    can_activate = False
    cycles: list[CycleRoute] = []

    while acquired != needed:
        cycle = CycleRoute(len(cycles) + 1)
        current = S.ClockTowerInterior
        current_time = T.DAY_1

        made_progress = True
        while made_progress:
            made_progress = False
            acquired_frozen = frozenset(acquired)

            available = []
            for cid in needed:
                if cid in acquired:
                    continue
                if not checks[cid].requires <= acquired:
                    continue
                ct = checks[cid].time
                if ct is None:
                    available.append(cid)
                elif any(t >= current_time for t in ct):
                    available.append(cid)

            if not available:
                break

            # Cache dijkstra from current position
            dist_from_current = world.dijkstra(current, acquired_frozen)

            def score(cid):
                c = checks[cid]
                travel_secs = dist_from_current.get(c.scene, float("inf"))

                # Also check SOS options
                if has_sos and activated_owls:
                    sos_cost, _ = _best_sos(current, c.scene, activated_owls, world, acquired_frozen)
                    travel_secs = min(travel_secs, sos_cost)

                if c.time is not None:
                    earliest = min(t for t in c.time if t >= current_time)
                    time_wait = earliest - current_time
                else:
                    time_wait = 0

                return (time_wait, travel_secs + c.duration)

            best_id = min(available, key=score)
            best = checks[best_id]

            if best.time is not None:
                earliest_valid = min(t for t in best.time if t >= current_time)
                current_time = earliest_valid

            travel_secs, path, _ = _travel(current, best.scene, has_sos, activated_owls, world, acquired_frozen)
            total_secs = travel_secs + best.duration

            cycle.add(best, total_secs, path)

            current = best.warp_to if best.warp_to else best.scene
            acquired.add(best_id)
            made_progress = True

            if best_id == Songs.Soaring:
                has_sos = True
            if best_id == M.Deku:
                can_activate = True
            if can_activate:
                for scene in path:
                    if scene in OWL_SCENES or _parent_scene(scene) in OWL_SCENES:
                        activated_owls.add(_parent_scene(scene))
                if best.warp_to:
                    ps = _parent_scene(best.warp_to)
                    if ps in OWL_SCENES:
                        activated_owls.add(ps)

        cycles.append(cycle)

        if not cycle.steps:
            missing = needed - acquired
            raise ValueError(f"Stuck! No checks possible. Missing: {missing}")

    return cycles
