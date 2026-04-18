from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Masks

def register(graph: GameGraph):
    graph.node(Scene.BeneathTheWell)

    graph.node(Scene.BeneathTheWell).check(
        Items.MirrorShield,
        requires={Masks.Gibdo, Items.BombBag, Items.Bottle, Items.MagicBeans, Items.Epona})

    graph.connect(Scene.BeneathTheWell, Scene.IkanaCastle, Strat("Walk", cost=30))
