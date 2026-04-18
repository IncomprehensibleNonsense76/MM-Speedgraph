from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks

walk = Strat("Walk", cost=30)

def register(graph: GameGraph):
    graph.node(Scene.GreatBayCoast, owl_statue=True)

    graph.node(Scene.GreatBayCoast).check(Masks.Zora, requires={Songs.Healing}, duration=90)

    graph.connect(Scene.GreatBayCoast, Scene.PiratesFortress,
                  Strat("Zora Swim", cost=30, requires=frozenset({Masks.Zora})))
    graph.connect(Scene.GreatBayCoast, Scene.MarineResearchLab, walk)
    graph.connect(Scene.GreatBayCoast, Scene.ZoraCape, walk)
    graph.connect(Scene.GreatBayCoast, Scene.PinnacleRock, walk)
    graph.connect(Scene.GreatBayCoast, Scene.OceanSpiderHouse, walk)
