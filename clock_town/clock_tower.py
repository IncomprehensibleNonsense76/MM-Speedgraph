from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks, TimeSlot

def register(graph: GameGraph):
    graph.node(Scene.ClockTowerInterior)
    graph.node(Scene.ClockTowerRooftop)

    # Checks
    graph.node(Scene.ClockTowerRooftop).check(
        Items.Ocarina, requires={Items.Magic}, time=frozenset({TimeSlot.NIGHT_3}))
    graph.node(Scene.ClockTowerRooftop).check(
        Songs.Time, requires={Items.Ocarina}, time=frozenset({TimeSlot.NIGHT_3}))
    graph.node(Scene.ClockTowerInterior).check(
        Songs.Healing, requires={Items.Ocarina, Songs.Time})
    graph.node(Scene.ClockTowerInterior).check(Masks.Deku, requires={Songs.Healing})
