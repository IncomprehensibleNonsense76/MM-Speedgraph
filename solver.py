from collections import deque, defaultdict
from model import Check
from enums import Scene as S, Masks as M, Songs, TimeSlot as T
from world import World, OWL_SCENES


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
    current: str, dest: str, activated_owls: set[str], dist: dict
) -> tuple[int, str | None]:
    """Find cheapest SOS warp: cost 1 to an owl, then walk to dest."""
    best_cost = float("inf")
    best_owl = None
    for owl in activated_owls:
        walk_from_owl = dist.get((owl, dest), float("inf"))
        total = 1 + walk_from_owl
        if total < best_cost:
            best_cost = total
            best_owl = owl
    return best_cost, best_owl


def _travel(current, dest, has_sos, activated_owls, dist, world):
    """Compute best travel option: walk, SOS, or SoT+walk. Returns (cost, path, method)."""
    if current == dest:
        return 0, [current], "stay"

    walk_cost = dist.get((current, dest), float("inf"))
    walk_path = world.path(current, dest) or [current]
    best_cost, best_path, method = walk_cost, walk_path, "walk"

    if has_sos and activated_owls:
        sos_cost, sos_owl = _best_sos(current, dest, activated_owls, dist)
        if sos_cost < best_cost:
            walk_seg = world.path(sos_owl, dest)
            if walk_seg and len(walk_seg) > 1:
                best_path = ["~SOS~"] + walk_seg
            else:
                best_path = ["~SOS~", dest]
            best_cost = sos_cost
            method = "sos"

    return best_cost, best_path, method


# =============================================================================
# Cycle-aware solver
# =============================================================================

class CycleRoute:
    """Result of one 3-day cycle."""
    def __init__(self, cycle_num):
        self.cycle_num = cycle_num
        self.steps: list[tuple[Check, int, list[str]]] = []  # (check, cost, path)
        self.total_cost = 0
        self.time = T.DAY_1

    def add(self, check, cost, path):
        self.steps.append((check, cost, path))
        self.total_cost += cost


def solve_route_cycles(
    checks: dict[str, Check],
    goals: list[str],
    world: World,
) -> list[CycleRoute]:
    """Greedy nearest-available solver with cycle + time slot support.

    Plans across multiple 3-day cycles. Song of Time resets position
    to Clock Tower Interior, Day 1. Items persist across cycles.
    """
    needed = _find_needed(checks, goals)
    dist = world.all_pairs()

    acquired: set[str] = set()
    activated_owls: set[str] = set()
    has_sos = False
    can_activate = False
    cycles: list[CycleRoute] = []

    while acquired != needed:
        cycle = CycleRoute(len(cycles) + 1)
        current = S.ClockTowerInterior
        current_time = T.DAY_1

        # Try to fill this cycle with checks
        made_progress = True
        while made_progress:
            made_progress = False

            # Find checks available right now
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

            # Pick nearest available, preferring checks at current time slot
            def score(cid):
                c = checks[cid]
                dest = c.scene
                cost, _, _ = _travel(current, dest, has_sos, activated_owls, dist, world)

                # Prefer checks at current time over future time
                if c.time is not None:
                    earliest = min(t for t in c.time if t >= current_time)
                    time_wait = earliest - current_time
                else:
                    time_wait = 0

                # Weight: travel cost + time slots we'd have to skip
                return (time_wait, cost)

            best_id = min(available, key=score)
            best = checks[best_id]

            # Advance time if needed
            if best.time is not None:
                earliest_valid = min(t for t in best.time if t >= current_time)
                current_time = earliest_valid

            # Travel
            cost, path, _ = _travel(current, best.scene, has_sos, activated_owls, dist, world)

            cycle.add(best, cost, path)
            current = best.scene
            acquired.add(best_id)
            made_progress = True

            # Track SOS / owl state
            if best_id == Songs.Soaring:
                has_sos = True
            if best_id == M.Deku:
                can_activate = True
            if can_activate:
                for scene in path:
                    if scene in OWL_SCENES:
                        activated_owls.add(scene)

        cycles.append(cycle)

        # Safety: if cycle made no progress, we're stuck
        if not cycle.steps:
            missing = needed - acquired
            raise ValueError(f"Stuck! No checks possible. Missing: {missing}")

    return cycles


# =============================================================================
# Legacy single-route solver (no time tracking)
# =============================================================================

def solve_route(
    checks: dict[str, Check],
    goals: list[str],
    world: World,
    start: str = S.ClockTowerInterior,
) -> tuple[list[tuple[Check, int, list[str]]], int]:
    """Greedy nearest-available solver (ignores time constraints)."""
    needed = _find_needed(checks, goals)
    dist = world.all_pairs()

    acquired: set[str] = set()
    activated_owls: set[str] = set()
    route: list[tuple[Check, int, list[str]]] = []
    current = start
    total_cost = 0

    has_sos = False
    can_activate = False

    while acquired != needed:
        available = [
            cid
            for cid in needed
            if cid not in acquired and checks[cid].requires <= acquired
        ]

        if not available:
            missing = needed - acquired
            raise ValueError(f"Stuck! No available checks. Missing: {missing}")

        def travel_cost(cid):
            dest = checks[cid].scene
            walk = dist.get((current, dest), float("inf"))
            if has_sos and activated_owls:
                sos_cost, _ = _best_sos(current, dest, activated_owls, dist)
                return min(walk, sos_cost)
            return walk

        best_id = min(available, key=travel_cost)
        best = checks[best_id]
        cost, path, _ = _travel(current, best.scene, has_sos, activated_owls, dist, world)

        total_cost += cost
        current = best.scene
        acquired.add(best_id)
        route.append((best, cost, path))

        if best_id == Songs.Soaring:
            has_sos = True
        if best_id == M.Deku:
            can_activate = True
        if can_activate:
            for scene in path:
                if scene in OWL_SCENES:
                    activated_owls.add(scene)

    return route, total_cost
