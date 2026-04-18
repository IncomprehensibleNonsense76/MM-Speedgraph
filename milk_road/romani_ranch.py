from __future__ import annotations
from core import GameGraph
from enums import Scene, Items, Masks, TimeSlot

def register(graph: GameGraph):
    graph.node(Scene.RomaniRanch)

    graph.node(Scene.RomaniRanch).check(Items.Epona, requires={Items.PowderKeg})
    graph.node(Scene.RomaniRanch).check(
        Items.BottleAliens, requires={Items.Bow, Items.Epona},
        time=frozenset({TimeSlot.NIGHT_1}))
    graph.node(Scene.RomaniRanch).check(Masks.BunnyHood, requires={Masks.Bremen, Items.Epona})
    graph.node(Scene.RomaniRanch).check(
        Masks.Romani, requires={Items.BottleAliens}, time=frozenset({TimeSlot.NIGHT_2}))
