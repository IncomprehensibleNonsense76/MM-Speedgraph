from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items

def register(graph: GameGraph):
    graph.node(Scene.MilkRoad, owl_statue=True)

    graph.connect(Scene.MilkRoad, Scene.RomaniRanch,
                  Strat("Powder Keg", cost=30, requires=frozenset({Items.PowderKeg})))
    graph.connect(Scene.MilkRoad, Scene.GormanTrack, Strat("Walk", cost=30))
