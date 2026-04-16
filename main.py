from checks import CHECKS, ANY_PERCENT_GOALS
from enums import Scene as S
from solver import solve_route
from world import World


def main():
    world = World()
    route, total_cost = solve_route(CHECKS, ANY_PERCENT_GOALS, world)

    print("=== Glitchless Any% Route (Greedy Nearest-Available + SOS) ===\n")

    current_scene = S.ClockTowerInterior
    step = 0
    sos_count = 0
    for check, cost, path in route:
        if check.scene != current_scene:
            step += 1
            is_sos = path[0] == "~SOS~"
            if is_sos:
                sos_count += 1
                travel = " -> ".join(path)
            else:
                travel = " -> ".join(path)
            print(f"\n  [{step}] {travel}  ({cost} loads)")
            current_scene = check.scene
        else:
            if step == 0:
                step += 1
                print(f"\n  [{step}] {check.scene}  (start)")
        print(f"       >> {check.name}")

    print(f"\n{'='*55}")
    print(f"  {len(route)} checks | {step} legs | {total_cost} scene loads | {sos_count} SOS warps")


if __name__ == "__main__":
    main()
