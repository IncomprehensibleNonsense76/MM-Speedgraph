from __future__ import annotations
from core import GameGraph
from enums import Scene, Items, Masks, TimeSlot

def register(graph: GameGraph):
    graph.node(Scene.GormanTrack)
    graph.node(Scene.GormanTrack).check(
        Masks.Garo, requires={Items.Epona},
        time=frozenset({TimeSlot.DAY_1, TimeSlot.DAY_2}))
