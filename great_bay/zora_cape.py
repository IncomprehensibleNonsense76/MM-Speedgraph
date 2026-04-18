from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks, Remains

def register(graph: GameGraph):
    graph.node(Scene.ZoraCape, owl_statue=True)

    graph.node(Scene.ZoraCape).check(Items.EnhancedDefense, requires={Remains.Gyorg})
    graph.node(Scene.ZoraCape).check(Items.BottleBeaver, requires={Masks.Zora, Items.Hookshot})

    graph.connect(Scene.ZoraCape, Scene.GreatBayTemple,
                  Strat("Turtle Ride", cost=30, requires=frozenset({Songs.NewWave})))
