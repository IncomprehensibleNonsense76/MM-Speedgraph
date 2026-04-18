from __future__ import annotations
from core import GameGraph

def register(graph: GameGraph):
    from ikana import (
        ikana_trail, ikana_canyon, ikana_graveyard,
        beneath_the_well, ikana_castle, stone_tower,
    )
    ikana_trail.register(graph)
    ikana_canyon.register(graph)
    ikana_graveyard.register(graph)
    beneath_the_well.register(graph)
    ikana_castle.register(graph)
    stone_tower.register(graph)
