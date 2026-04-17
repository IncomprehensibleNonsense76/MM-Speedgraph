"""CLI entry point for the route solver.

Usage:
    python run.py [goal] [--ruleset NAME] [--version NAME] [--platform NAME]

Goals: any%, bottles, masks
"""

from __future__ import annotations
import sys
from graph import build
from core import Ruleset, Version, Platform
from enums import Events, Items, Masks
from route_solver import solve, print_route

GOALS = {
    "any%": ("Glitchless Any%", [Events.KillMajora]),
    "bottles": ("All Bottles", [
        Items.Bottle, Items.BottleAliens, Items.BottleGoldDust,
        Items.BottleGraveyard, Items.BottleBeaver, Items.BottleMadameAroma,
    ]),
    "masks": ("All Masks", [Masks.FierceDeity]),
}


def main():
    goal_key = "any%"
    ruleset = Ruleset.GLITCHLESS
    version = Version.EN
    platform = Platform.N64

    args = sys.argv[1:]
    for arg in args:
        if arg in GOALS:
            goal_key = arg
        elif arg.startswith("--ruleset="):
            ruleset = Ruleset[arg.split("=")[1].upper()]
        elif arg.startswith("--version="):
            version = Version[arg.split("=")[1].upper()]
        elif arg.startswith("--platform="):
            platform = Platform[arg.split("=")[1].upper()]

    if goal_key not in GOALS:
        print(f"Unknown goal: {goal_key}")
        print(f"Available: {', '.join(GOALS.keys())}")
        return

    goal_name, goal_list = GOALS[goal_key]

    graph = build(ruleset=ruleset, version=version, platform=platform)
    print(f"Graph: {graph.stats()}\n")

    cycles = solve(graph, goal_list)
    print_route(goal_name, cycles, graph)


if __name__ == "__main__":
    main()
