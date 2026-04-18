from __future__ import annotations
from core import GameGraph
from enums import Scene, Items, Masks

def register(graph: GameGraph):
    graph.node(Scene.PiratesFortress)
    graph.node(Scene.PiratesFortress).check(Items.Hookshot, requires={Masks.Zora, Masks.Goron})
