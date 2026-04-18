from __future__ import annotations
from core import GameGraph
from enums import Scene, Items, Songs, Masks

def register(graph: GameGraph):
    graph.node(Scene.MarineResearchLab)
    graph.node(Scene.MarineResearchLab).check(
        Songs.NewWave,
        requires={Masks.Zora, Items.Hookshot, Items.Bottle, Items.BottleAliens, Items.BottleGoldDust})
