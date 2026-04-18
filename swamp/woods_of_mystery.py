from __future__ import annotations
from core import GameGraph
from enums import Scene

def register(graph: GameGraph):
    graph.node(Scene.WoodsOfMystery)
