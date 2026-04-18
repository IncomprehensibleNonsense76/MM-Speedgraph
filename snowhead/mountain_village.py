from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks

walk = Strat("Walk", cost=30)

def register(graph: GameGraph):
    graph.node(Scene.MountainVillage, owl_statue=True)

    graph.node(Scene.MountainVillage).check(
        Masks.Goron, requires={Items.LensOfTruth, Songs.Healing}, duration=90)
    graph.node(Scene.MountainVillage).check(Masks.DonGero, requires={Masks.Goron})
    graph.node(Scene.MountainVillage).check(Items.RazorSword, requires={Items.FireArrows})
    graph.node(Scene.MountainVillage).check(
        Items.GildedSword, requires={Items.RazorSword, Items.GoldDust})

    # Upgrades
    graph.node(Scene.MountainVillage).check(Items.BombBag40, requires={Items.BombBag30, Masks.Goron})

    graph.connect(Scene.MountainVillage, Scene.PathToGoronVillage, walk)
    graph.connect(Scene.MountainVillage, Scene.PathToSnowhead, walk)
