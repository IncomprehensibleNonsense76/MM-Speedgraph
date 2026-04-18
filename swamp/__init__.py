from __future__ import annotations
from core import GameGraph

def register(graph: GameGraph):
    from swamp import (
        southern_swamp, deku_palace, woodfall,
        woods_of_mystery, hags_potion_shop,
        swamp_spider_house, deku_princess_prison,
    )
    southern_swamp.register(graph)
    deku_palace.register(graph)
    woodfall.register(graph)
    woods_of_mystery.register(graph)
    hags_potion_shop.register(graph)
    swamp_spider_house.register(graph)
    deku_princess_prison.register(graph)
