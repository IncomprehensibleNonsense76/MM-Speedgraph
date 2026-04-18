from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Masks

def register(graph: GameGraph):
    graph.node(Scene.IkanaTrail)

    graph.node(Scene.IkanaTrail).check(Masks.Stone, requires={Items.LensOfTruth, Items.Bottle})

    # To Graveyard: Epona or Goron+Bombs (before Garo gate)
    graph.connect(Scene.IkanaTrail, Scene.IkanaGraveyard,
                  Strat("Epona", cost=30, requires=frozenset({Items.Epona})))
    graph.connect(Scene.IkanaTrail, Scene.IkanaGraveyard,
                  Strat("Goron Damage Boost", cost=30,
                        requires=frozenset({Masks.Goron, Items.BombBag})))

    # To Canyon: full gate
    graph.connect(Scene.IkanaTrail, Scene.IkanaCanyon,
                  Strat("Garo + Hookshot + Epona", cost=30,
                        requires=frozenset({Masks.Garo, Items.Hookshot, Items.Epona})))
    graph.connect(Scene.IkanaTrail, Scene.IkanaCanyon,
                  Strat("Garo + Hookshot + Goron Boost", cost=30,
                        requires=frozenset({Masks.Garo, Items.Hookshot, Masks.Goron, Items.BombBag})))
