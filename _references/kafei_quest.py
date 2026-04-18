"""Anju & Kafei quest — spans all 3 days within a cycle."""

from __future__ import annotations
from core import GameGraph
from enums import Scene, Items, Masks, TimeSlot

N1 = frozenset({TimeSlot.NIGHT_1})
D2 = frozenset({TimeSlot.DAY_2})
D3 = frozenset({TimeSlot.DAY_3})
N3 = frozenset({TimeSlot.NIGHT_3})


def register(graph: GameGraph):
    # Step 1-2: Midnight meeting with Anju -> Letter to Kafei
    graph.node(Scene.EastClockTown).check(
        Items.LetterToKafei, requires={Masks.KafeiMask, Items.RoomKey}, time=N1)

    # Step 3-4: Find Kafei Day 2 -> Pendant of Memories
    graph.node(Scene.LaundryPool).check(
        Items.PendantOfMemories, requires={Items.LetterToKafei}, time=D2)

    # Step 5-6: Day 3 hideout -> Priority Mail + Keaton Mask
    graph.node(Scene.LaundryPool).check(
        Items.PriorityMail, requires={Items.PendantOfMemories}, time=D3)
    graph.node(Scene.LaundryPool).check(
        Masks.Keaton, requires={Items.PendantOfMemories}, time=D3)

    # Step 7 (EXCLUSIVE per cycle):
    graph.node(Scene.WestClockTown).check(
        Masks.Postman, requires={Items.PriorityMail}, time=N3)
    graph.node(Scene.EastClockTown).check(
        Items.BottleMadameAroma, requires={Items.PriorityMail, Masks.Romani}, time=N3)

    # Step 8-9: Couple's Mask
    graph.node(Scene.EastClockTown).check(
        Masks.Couple,
        requires={Items.PendantOfMemories, Masks.Garo, Items.Hookshot}, time=N3)
