from __future__ import annotations
from core import GameGraph
from enums import Scene, Items, TimeSlot

def register(graph: GameGraph):
    graph.node(Scene.OceanSpiderHouse)
    graph.node(Scene.OceanSpiderHouse).check(
        Items.GiantWallet, requires={Items.Epona}, time=frozenset({TimeSlot.DAY_1}))
