from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks, TimeSlot

walk = Strat("Walk", cost=30)

N1 = frozenset({TimeSlot.NIGHT_1})
N2 = frozenset({TimeSlot.NIGHT_2})
D1_D2 = frozenset({TimeSlot.DAY_1, TimeSlot.DAY_2})


def register(graph: GameGraph):
    graph.node(Scene.MilkRoad, owl_statue=True)
    graph.node(Scene.RomaniRanch)
    graph.node(Scene.GormanTrack)

    # === Checks ===
    graph.node(Scene.RomaniRanch).check(Items.Epona, requires={Items.PowderKeg})
    graph.node(Scene.RomaniRanch).check(
        Items.BottleAliens, requires={Items.Bow, Items.Epona}, time=N1)
    graph.node(Scene.RomaniRanch).check(
        Masks.BunnyHood, requires={Masks.Bremen, Items.Epona})
    graph.node(Scene.RomaniRanch).check(
        Masks.Romani, requires={Items.BottleAliens}, time=N2)
    graph.node(Scene.GormanTrack).check(
        Masks.Garo, requires={Items.Epona}, time=D1_D2)

    # === Traversals ===
    # Ranch — gated by Powder Keg
    graph.connect(Scene.MilkRoad, Scene.RomaniRanch,
                  Strat("Powder Keg", cost=30, requires=frozenset({Items.PowderKeg})))
    graph.connect(Scene.MilkRoad, Scene.GormanTrack, walk)
