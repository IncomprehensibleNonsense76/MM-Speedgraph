from __future__ import annotations
from core import GameGraph

def register(graph: GameGraph):
    from great_bay import (
        great_bay_coast, pirates_fortress, marine_research_lab,
        zora_cape, pinnacle_rock, ocean_spider_house,
    )
    great_bay_coast.register(graph)
    pirates_fortress.register(graph)
    marine_research_lab.register(graph)
    zora_cape.register(graph)
    pinnacle_rock.register(graph)
    ocean_spider_house.register(graph)
