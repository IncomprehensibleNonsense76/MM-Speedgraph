from __future__ import annotations
from core import GameGraph
from enums import Scene, Items, Songs

def register(graph: GameGraph):
    graph.node(Scene.IkanaCastle)
    graph.node(Scene.IkanaCastle).check(Songs.Elegy, requires={Items.MirrorShield, Items.PowderKeg})
