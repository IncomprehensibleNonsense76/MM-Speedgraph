from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Remains

def register(graph: GameGraph):
    graph.node(Scene.DekuPrincessPrison)

    graph.node(Scene.DekuPrincessPrison).check(Songs.OathToOrder, requires={Remains.Odolwa})
    graph.node(Scene.DekuPrincessPrison).check(
        Items.DekuPrincess, requires={Remains.Odolwa, Items.Bottle})

    graph.connect(Scene.DekuPrincessPrison, Scene.Woodfall, Strat("Walk", cost=30))
