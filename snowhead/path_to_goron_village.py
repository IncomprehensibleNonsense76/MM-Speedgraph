from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene

walk = Strat("Walk", cost=30)

def register(graph: GameGraph):
    graph.node(Scene.PathToGoronVillage)
    graph.connect(Scene.PathToGoronVillage, Scene.GoronVillage, walk)
    graph.connect(Scene.PathToGoronVillage, Scene.GoronRacetrack, walk)
