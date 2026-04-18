from __future__ import annotations
from core import GameGraph
from enums import Scene, Items, Masks

def register(graph: GameGraph):
    graph.node(Scene.SwampSpiderHouse)
    graph.node(Scene.SwampSpiderHouse).check(
        Masks.Truth, requires={Masks.Deku, Items.Bottle, Items.Bow})
