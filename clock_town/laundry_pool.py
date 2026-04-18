from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Masks, TimeSlot

ANY_NIGHT = frozenset({TimeSlot.NIGHT_1, TimeSlot.NIGHT_2, TimeSlot.NIGHT_3})

def register(graph: GameGraph):
    graph.node(Scene.LaundryPool)

    graph.node(Scene.LaundryPool).check(Items.StrayFairyCT)
    graph.node(Scene.LaundryPool).check(Masks.Bremen, requires={Masks.Deku}, time=ANY_NIGHT)

    # Kafei quest checks
    graph.node(Scene.LaundryPool).check(
        Items.PendantOfMemories, requires={Items.LetterToKafei},
        time=frozenset({TimeSlot.DAY_2}))
    graph.node(Scene.LaundryPool).check(
        Items.PriorityMail, requires={Items.PendantOfMemories},
        time=frozenset({TimeSlot.DAY_3}))
    graph.node(Scene.LaundryPool).check(
        Masks.Keaton, requires={Items.PendantOfMemories},
        time=frozenset({TimeSlot.DAY_3}))
