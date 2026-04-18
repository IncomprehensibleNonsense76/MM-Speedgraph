from __future__ import annotations
from core import GameGraph, Strat, Ruleset
from enums import Scene, Items, Masks, Songs, TimeSlot

TF_WEIGHT = 45


def register(graph: GameGraph):
    graph.node(Scene.TerminaField)

    # === Clock Town <-> Termina Field ===
    graph.connect(Scene.SouthClockTown, Scene.TerminaField, Strat("Walk", cost=30))

    # === Termina Field exits ===
    graph.connect(Scene.TerminaField, Scene.SouthernSwamp,
                  Strat("Backwalk + CS", cost=180))

    graph.connect(Scene.TerminaField, Scene.PathToMountainVillage,
                  Strat("Walk", cost=TF_WEIGHT))

    # Great Bay — need Epona or Goron+Bombs to cross fence
    graph.connect(Scene.TerminaField, Scene.GreatBayCoast,
                  Strat("Epona", cost=TF_WEIGHT, requires=frozenset({Items.Epona})))
    graph.connect(Scene.TerminaField, Scene.GreatBayCoast,
                  Strat("Goron Damage Boost", cost=TF_WEIGHT,
                        requires=frozenset({Masks.Goron, Items.BombBag})))

    graph.connect(Scene.TerminaField, Scene.MilkRoad,
                  Strat("Walk", cost=TF_WEIGHT))

    graph.connect(Scene.TerminaField, Scene.IkanaTrail,
                  Strat("Walk", cost=TF_WEIGHT))

    # === Kamaro's Mask (overworld check) ===
    graph.node(Scene.TerminaField).check(
        Masks.Kamaro, requires={Songs.Healing},
        time=frozenset({TimeSlot.NIGHT_1, TimeSlot.NIGHT_2, TimeSlot.NIGHT_3}))
