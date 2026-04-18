from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Masks, TimeSlot

def register(graph: GameGraph):
    graph.node(Scene.NorthClockTown)
    graph.node(Scene.NorthClockTown).check(
        Masks.Blast, requires={Masks.Deku}, time=frozenset({TimeSlot.NIGHT_1}))

    graph.connect(Scene.NorthClockTown, Scene.EastClockTown, Strat("Walk", cost=30))
    graph.connect(Scene.NorthClockTown, Scene.CTGreatFairyFountain, Strat("Walk", cost=30))
