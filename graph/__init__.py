"""Game graph builder — assembles the full MM world from region modules.

Each module in this package has a register(graph) function that adds
its nodes, checks, and traversal strats to the GameGraph.
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

    # Register overworld regions
    from graph import clock_town
    from graph import southern_swamp
    from graph import mountain
    from graph import great_bay
    from graph import milk_road
    from graph import ikana
    from graph import overworld
    from graph import moon

    from graph import kafei_quest, upgrades

    clock_town.register(graph)
    overworld.register(graph)
    southern_swamp.register(graph)
    mountain.register(graph)
    milk_road.register(graph)
    great_bay.register(graph)
    ikana.register(graph)
    moon.register(graph)
    kafei_quest.register(graph)
    upgrades.register(graph)

    # Register dungeons
    from graph.dungeons import wft, sht, gbt, stt

    wft.register(graph)
    sht.register(graph)
    gbt.register(graph)
    stt.register(graph)

    return graph
