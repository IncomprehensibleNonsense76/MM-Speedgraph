"""Game graph builder — assembles the full MM world from region modules.

Region modules match the kz warp menu categories:
  clock_town, swamp, snowhead, great_bay, ikana,
  overworld, milk_road, moon, other

Each module has a register(graph) function that adds its nodes,
checks, and traversal strats to the GameGraph.
"""

from __future__ import annotations
from core import GameGraph, Ruleset, Version, Platform


def build(
    ruleset: Ruleset = Ruleset.GLITCHLESS,
    version: Version = Version.EN,
    platform: Platform = Platform.N64,
) -> GameGraph:
    """Build the complete game graph with all regions and dungeons."""
    graph = GameGraph(ruleset=ruleset, version=version, platform=platform)

    # Regions (kz warp menu order)
    from graph import clock_town
    from graph import swamp
    from graph import snowhead
    from graph import great_bay
    from graph import ikana
    from graph import overworld
    from graph import milk_road
    from graph import moon

    clock_town.register(graph)
    overworld.register(graph)
    swamp.register(graph)
    snowhead.register(graph)
    milk_road.register(graph)
    great_bay.register(graph)
    ikana.register(graph)
    moon.register(graph)

    # Cross-region quests and upgrades
    from graph import kafei_quest, upgrades

    kafei_quest.register(graph)
    upgrades.register(graph)

    # Dungeons
    from graph.dungeons import wft, sht, gbt, stt

    wft.register(graph)
    sht.register(graph)
    gbt.register(graph)
    stt.register(graph)

    return graph
