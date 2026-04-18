from __future__ import annotations
from core import GameGraph
from enums import Scene, Songs, Masks

def register(graph: GameGraph):
    graph.node(Scene.GoronShrine)
    graph.node(Scene.GoronShrine).check(Songs.Lullaby, requires={Songs.LullabyIntro, Masks.Goron})
