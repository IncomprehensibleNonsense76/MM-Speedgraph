"""Game graph builder — assembles the full MM world from region modules.

Region modules match the kz warp menu categories:
  clock_town, swamp, snowhead, great_bay, ikana,
  overworld, milk_road, moon

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
    from clock_town import register as reg_ct
    from swamp import register as reg_swamp
    from snowhead import register as reg_snowhead
    from great_bay import register as reg_gb
    from ikana import register as reg_ikana
    from overworld import register as reg_ow
    from milk_road import register as reg_mr
    from moon import register as reg_moon

    reg_ct(graph)
    reg_ow(graph)
    reg_swamp(graph)
    reg_snowhead(graph)
    reg_mr(graph)
    reg_gb(graph)
    reg_ikana(graph)
    reg_moon(graph)

    # Dungeons
    from dungeons import wft, sht, gbt, stt
    wft.register(graph)
    sht.register(graph)
    gbt.register(graph)
    stt.register(graph)

    return graph
