from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Masks, TimeSlot

ANY_NIGHT = frozenset({TimeSlot.NIGHT_1, TimeSlot.NIGHT_2, TimeSlot.NIGHT_3})

def register(graph: GameGraph):
    graph.node(Scene.WestClockTown)

    graph.node(Scene.WestClockTown).check(Items.BombBag)
    graph.node(Scene.WestClockTown).check(Masks.AllNight, requires={Masks.Blast},
                                           time=frozenset({TimeSlot.NIGHT_3}))
    graph.node(Scene.WestClockTown).check(Items.AdultWallet)

    # Upgrades
    graph.node(Scene.WestClockTown).check(Items.BombBag30, requires={Items.BombBag, Masks.Blast})
    graph.node(Scene.WestClockTown).check(Items.BottleGoldDust, requires={Items.GoldDust}, time=ANY_NIGHT)

    # Kafei quest
    graph.node(Scene.WestClockTown).check(
        Masks.Postman, requires={Items.PriorityMail}, time=frozenset({TimeSlot.NIGHT_3}))
