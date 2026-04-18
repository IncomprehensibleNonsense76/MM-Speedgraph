from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks, Remains

def register(graph: GameGraph):
    graph.node(Scene.Snowhead, owl_statue=True)
    graph.node(Scene.Snowhead).check(Items.DoubleMagic, requires={Remains.Goht})

    graph.connect(Scene.Snowhead, Scene.SnowheadTemple,
                  Strat("Goron Lullaby", cost=30,
                        requires=frozenset({Masks.Goron, Songs.Lullaby})))
