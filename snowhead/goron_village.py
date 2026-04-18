from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks

walk = Strat("Walk", cost=30)

def register(graph: GameGraph):
    graph.node(Scene.GoronVillage)

    graph.node(Scene.GoronVillage).check(Songs.LullabyIntro, requires={Masks.Goron})
    graph.node(Scene.GoronVillage).check(Items.PowderKeg, requires={Masks.Goron, Items.FireArrows})

    graph.connect(Scene.GoronVillage, Scene.GoronShrine, walk)
    graph.connect(Scene.GoronVillage, Scene.LonePeakShrine, walk)
