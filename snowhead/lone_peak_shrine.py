from __future__ import annotations
from core import GameGraph
from enums import Scene, Items

def register(graph: GameGraph):
    graph.node(Scene.LonePeakShrine)
    graph.node(Scene.LonePeakShrine).check(
        Items.LensOfTruth, requires={Items.Magic, Items.Bow, Items.BombBag})
