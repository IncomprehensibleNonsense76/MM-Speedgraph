from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Masks, Songs, TimeSlot

def register(graph: GameGraph):
    graph.node(Scene.EastClockTown)

    # Checks
    graph.node(Scene.EastClockTown).check(Masks.KafeiMask, requires={Masks.Deku})
    graph.node(Scene.EastClockTown).check(Items.BombersNotebook, requires={Masks.Deku, Items.Magic})
    graph.node(Scene.EastClockTown).check(Items.RoomKey, requires={Masks.Deku})

    # Kafei quest checks at this location
    graph.node(Scene.EastClockTown).check(
        Items.LetterToKafei, requires={Masks.KafeiMask, Items.RoomKey},
        time=frozenset({TimeSlot.NIGHT_1}))
    graph.node(Scene.EastClockTown).check(
        Items.BottleMadameAroma, requires={Items.PriorityMail, Masks.Romani},
        time=frozenset({TimeSlot.NIGHT_3}))
    graph.node(Scene.EastClockTown).check(
        Masks.Couple, requires={Items.PendantOfMemories, Masks.Garo, Items.Hookshot},
        time=frozenset({TimeSlot.NIGHT_3}))

    # Upgrades at this location
    graph.node(Scene.EastClockTown).check(Items.Quiver40, requires={Items.Bow})

    # Circus Leader's Mask (Milk Bar)
    graph.node(Scene.EastClockTown).check(
        Masks.CircusLeader,
        requires={Masks.Romani, Masks.Deku, Masks.Goron, Masks.Zora, Items.Ocarina})

    # Edge to Observatory
    graph.connect(Scene.EastClockTown, Scene.Observatory, Strat("Walk", cost=30))
