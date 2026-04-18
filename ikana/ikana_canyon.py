from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks, Remains

walk = Strat("Walk", cost=30)

def register(graph: GameGraph):
    graph.node(Scene.IkanaCanyon, owl_statue=True)

    graph.node(Scene.IkanaCanyon).check(Masks.Gibdo, requires={Songs.Storms, Songs.Healing})
    graph.node(Scene.IkanaCanyon).check(Items.GreatFairySword, requires={Remains.Twinmold})

    graph.connect(Scene.IkanaCanyon, Scene.IkanaGraveyard, walk)
    graph.connect(Scene.IkanaCanyon, Scene.BeneathTheWell, walk)
    graph.connect(Scene.IkanaCanyon, Scene.StoneTower, walk)
