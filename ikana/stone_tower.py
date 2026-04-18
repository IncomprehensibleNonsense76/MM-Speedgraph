from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Songs, Masks

def register(graph: GameGraph):
    graph.node(Scene.StoneTower, owl_statue=True)

    graph.connect(Scene.StoneTower, Scene.StoneTowerTemple,
                  Strat("Elegy Statues", cost=30,
                        requires=frozenset({Songs.Elegy, Masks.Goron, Masks.Zora, Masks.Deku})))
