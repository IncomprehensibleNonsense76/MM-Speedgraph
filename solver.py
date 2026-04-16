from collections import deque, defaultdict
from model import Check
from enums import Scene as S, Masks as M, Songs
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


def resolve(checks: dict[str, Check], goals: list[str]) -> list[Check]:
    """Pure dependency order (no travel cost). Tiebreak alphabetically."""
    needed = _find_needed(checks, goals)

    in_deg: dict[str, int] = {cid: 0 for cid in needed}
    fwd: dict[str, list[str]] = defaultdict(list)

    for cid in needed:
        for req in checks[cid].requires:
            if req in needed:
                in_deg[cid] += 1
                fwd[req].append(cid)

    ready = deque(sorted(cid for cid, d in in_deg.items() if d == 0))
    order: list[Check] = []

    while ready:
        cid = ready.popleft()
        order.append(checks[cid])
        for dep in sorted(fwd[cid]):
            in_deg[dep] -= 1
            if in_deg[dep] == 0:
                ready.append(dep)

    if len(order) != len(needed):
        cycle = needed - {c.id for c in order}
        raise ValueError(f"Cycle detected among: {cycle}")

    return order


def _best_sos(current: str, dest: str, activated_owls: set[str],
              dist: dict) -> tuple[int, str | None]:
    """Find cheapest SOS warp: cost 1 to an owl, then walk to dest.
    Returns (cost, owl_scene) or (inf, None) if no warp helps."""
    best_cost = float("inf")
    best_owl = None
    for owl in activated_owls:
        walk_from_owl = dist.get((owl, dest), float("inf"))
        total = 1 + walk_from_owl
        if total < best_cost:
            best_cost = total
            best_owl = owl
    return best_cost, best_owl


def solve_route(
    checks: dict[str, Check],
    goals: list[str],
    world: World,
    start: str = S.ClockTowerInterior,
) -> tuple[list[tuple[Check, int, list[str]]], int]:
    """Greedy nearest-available solver with SOS warp support.

    Returns (route, total_cost) where route is a list of
    (check, leg_cost, path_through_scenes) tuples.
    """
    needed = _find_needed(checks, goals)
    dist = world.all_pairs()

    acquired: set[str] = set()
    activated_owls: set[str] = set()
    route: list[tuple[Check, int, list[str]]] = []
    current = start
    total_cost = 0

    has_sos = False
    can_activate = False  # need deku_mask (human + sword)

    while acquired != needed:
        # All checks whose dependencies are satisfied
        available = [
            cid for cid in needed
            if cid not in acquired
            and checks[cid].requires <= acquired
        ]

        if not available:
            missing = needed - acquired
            raise ValueError(f"Stuck! No available checks. Missing: {missing}")

        # Compute travel cost for each available check
        def travel_cost(cid):
            dest = checks[cid].scene
            walk = dist.get((current, dest), float("inf"))
            if has_sos and activated_owls:
                sos_cost, _ = _best_sos(current, dest, activated_owls, dist)
                return min(walk, sos_cost)
            return walk

        best_id = min(available, key=travel_cost)
        best = checks[best_id]
        dest = best.scene

        # Determine walk vs SOS
        walk_cost = dist.get((current, dest), 0) if current != dest else 0
        used_sos = False
        sos_owl = None

        if has_sos and activated_owls and current != dest:
            sos_cost, sos_owl = _best_sos(current, dest, activated_owls, dist)
            if sos_cost < walk_cost:
                walk_cost = sos_cost
                used_sos = True

        # Build path for display
        if current == dest:
            path = [current]
        elif used_sos:
            walk_segment = world.path(sos_owl, dest)
            if walk_segment and len(walk_segment) > 1:
                path = ["~SOS~"] + walk_segment
            else:
                path = ["~SOS~", dest]
        else:
            path = world.path(current, dest) or [current]

        cost = walk_cost
        total_cost += cost
        current = dest
        acquired.add(best_id)
        route.append((best, cost, path))

        # Track SOS state
        if best_id == Songs.Soaring:
            has_sos = True
        if best_id == M.Deku:
            can_activate = True

        # Activate owls along the traversed path (if human form available)
        if can_activate:
            for scene in path:
                if scene in OWL_SCENES:
                    activated_owls.add(scene)

    return route, total_cost
