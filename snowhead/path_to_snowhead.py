from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene

def register(graph: GameGraph):
    graph.node(Scene.PathToSnowhead)
    graph.connect(Scene.PathToSnowhead, Scene.Snowhead, Strat("Walk", cost=30))
