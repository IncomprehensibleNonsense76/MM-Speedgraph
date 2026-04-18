import sys
from checks import CHECKS
from enums import Scene as S, TimeSlot as T
from solver import solve_route_cycles, _fmt_time
from world import World
import goals

TIME_NAMES = {
    T.DAY_1: "Day 1",
    T.NIGHT_1: "Night 1",
    T.DAY_2: "Day 2",
    T.NIGHT_2: "Night 2",
    T.DAY_3: "Day 3",
    T.NIGHT_3: "Night 3",
}

GOAL_SETS = {
    "any%": ("Glitchless Any%", goals.ANY_PERCENT),
    "bottles": ("All Bottles", goals.ALL_BOTTLES),
    "masks": ("All Masks", goals.ALL_MASKS),
}


def print_cycle_route(goal_name, cycles):
    print(f"=== {goal_name} (Cycle-Aware Solver) ===")

    total_time = 0
    total_checks = 0
    total_sos = 0

    for cycle in cycles:
        print(f"\n{'─' * 60}")
        print(f"  CYCLE {cycle.cycle_num} (start: Clock Tower Interior, Day 1)")
        print(f"{'─' * 60}")

        current_scene = S.ClockTowerInterior
        step = 0
        last_time = None

        for check, cost, path in cycle.steps:
            if check.time is not None:
                earliest = min(check.time)
                if last_time is None or earliest > last_time:
                    last_time = earliest
                    print(f"\n  --- {TIME_NAMES[earliest]} ---")

            if check.scene != current_scene:
                step += 1
                is_sos = path[0] == "~SOS~"
                if is_sos:
                    total_sos += 1
                travel = " -> ".join(path)
                print(f"\n  [{step}] {travel}  ({_fmt_time(cost)})")
                current_scene = check.warp_to or check.scene
            else:
                if step == 0:
                    step += 1
                    print(f"\n  [{step}] {check.scene}  (start)")
                elif cost > 0:
                    print(f"       (+{_fmt_time(cost)})")
                current_scene = check.warp_to or check.scene
            print(f"       >> {check.name}")

            if check.warp_to and check.warp_to != check.scene:
                print(f"       ~~ warp to {check.warp_to}")

        total_time += cycle.total_cost
        total_checks += len(cycle.steps)

        if cycle.cycle_num < len(cycles):
            print(f"\n  >> Song of Time -> Clock Tower Interior, Day 1")

    print(f"\n{'=' * 60}")
    m, s = divmod(total_time, 60)
    print(
        f"  {total_checks} checks | {len(cycles)} cycles | {_fmt_time(total_time)} ({total_time}s) | {total_sos} SOS"
    )


def main():
    goal_key = sys.argv[1] if len(sys.argv) > 1 else "any%"

    if goal_key not in GOAL_SETS:
        print(f"Unknown goal: {goal_key}")
        print(f"Available: {', '.join(GOAL_SETS.keys())}")
        return

    goal_name, goal_list = GOAL_SETS[goal_key]
    world = World()
    cycles = solve_route_cycles(CHECKS, goal_list, world)
    print_cycle_route(goal_name, cycles)


if __name__ == "__main__":
    main()
