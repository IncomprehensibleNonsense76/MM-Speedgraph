from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks, TimeSlot

TF_WEIGHT = 45
ANY_NIGHT = frozenset({TimeSlot.NIGHT_1, TimeSlot.NIGHT_2, TimeSlot.NIGHT_3})

def register(graph: GameGraph):
    graph.node(Scene.TerminaField)

    graph.node(Scene.TerminaField).check(Masks.Kamaro, requires={Songs.Healing}, time=ANY_NIGHT)

    # TF exits
    graph.connect(Scene.TerminaField, Scene.SouthernSwamp,
                  Strat("Backwalk + CS", cost=180))
    graph.connect(Scene.TerminaField, Scene.PathToMountainVillage,
                  Strat("Walk", cost=TF_WEIGHT))
    graph.connect(Scene.TerminaField, Scene.GreatBayCoast,
                  Strat("Epona", cost=TF_WEIGHT, requires=frozenset({Items.Epona})))
    graph.connect(Scene.TerminaField, Scene.GreatBayCoast,
                  Strat("Goron Damage Boost", cost=TF_WEIGHT,
                        requires=frozenset({Masks.Goron, Items.BombBag})))
    graph.connect(Scene.TerminaField, Scene.MilkRoad, Strat("Walk", cost=TF_WEIGHT))
    graph.connect(Scene.TerminaField, Scene.IkanaTrail, Strat("Walk", cost=TF_WEIGHT))
