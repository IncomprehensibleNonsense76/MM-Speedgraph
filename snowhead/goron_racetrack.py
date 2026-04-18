from __future__ import annotations
from core import GameGraph
from enums import Scene, Items, Masks, Remains

def register(graph: GameGraph):
    graph.node(Scene.GoronRacetrack)
    graph.node(Scene.GoronRacetrack).check(Items.GoldDust, requires={Masks.Goron, Remains.Goht})
