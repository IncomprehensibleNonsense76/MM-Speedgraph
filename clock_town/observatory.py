from __future__ import annotations
from core import GameGraph
from enums import Scene, Items

def register(graph: GameGraph):
    graph.node(Scene.Observatory)
    graph.node(Scene.Observatory).check(Items.MoonsTear, requires={Items.Magic})
