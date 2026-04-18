from __future__ import annotations
from core import GameGraph

def register(graph: GameGraph):
    from clock_town import (
        south_clock_town, north_clock_town, east_clock_town,
        west_clock_town, laundry_pool, clock_tower,
        fairy_fountain, observatory,
    )
    south_clock_town.register(graph)
    north_clock_town.register(graph)
    east_clock_town.register(graph)
    west_clock_town.register(graph)
    laundry_pool.register(graph)
    clock_tower.register(graph)
    fairy_fountain.register(graph)
    observatory.register(graph)
