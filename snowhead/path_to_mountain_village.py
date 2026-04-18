from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items

def register(graph: GameGraph):
    graph.node(Scene.PathToMountainVillage)
    graph.connect(Scene.PathToMountainVillage, Scene.MountainVillage,
                  Strat("Clear Path", cost=30, requires=frozenset({Items.Bow, Items.BombBag})))
