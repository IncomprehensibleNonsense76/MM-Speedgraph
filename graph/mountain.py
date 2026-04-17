from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks, Remains

walk = Strat("Walk", cost=30)


def register(graph: GameGraph):
    graph.node(Scene.PathToMountainVillage)
    graph.node(Scene.MountainVillage, owl_statue=True)
    graph.node(Scene.PathToGoronVillage)
    graph.node(Scene.GoronVillage)
    graph.node(Scene.GoronShrine)
    graph.node(Scene.GoronRacetrack)
    graph.node(Scene.LonePeakShrine)
    graph.node(Scene.PathToSnowhead)
    graph.node(Scene.Snowhead, owl_statue=True)

    # === Checks ===
    graph.node(Scene.LonePeakShrine).check(Items.LensOfTruth, requires={Items.Magic})
    graph.node(Scene.MountainVillage).check(
        Masks.Goron, requires={Items.LensOfTruth, Songs.Healing}, duration=90)
    graph.node(Scene.MountainVillage).check(Masks.DonGero, requires={Masks.Goron})
    graph.node(Scene.GoronVillage).check(Songs.LullabyIntro, requires={Masks.Goron})
    graph.node(Scene.GoronShrine).check(Songs.Lullaby, requires={Songs.LullabyIntro, Masks.Goron})
    graph.node(Scene.GoronVillage).check(Items.PowderKeg, requires={Masks.Goron, Items.FireArrows})
    graph.node(Scene.GoronRacetrack).check(Items.GoldDust, requires={Masks.Goron, Remains.Goht})
    graph.node(Scene.Snowhead).check(Items.DoubleMagic, requires={Remains.Goht})
    graph.node(Scene.MountainVillage).check(Items.RazorSword, requires={Items.FireArrows})
    graph.node(Scene.MountainVillage).check(
        Items.GildedSword, requires={Items.RazorSword, Items.GoldDust})

    # === Traversals ===
    # Path to Mtn Village — gated by bow (ice) + bombs (boulders)
    graph.connect(Scene.PathToMountainVillage, Scene.MountainVillage,
                  Strat("Clear Path", cost=30, requires=frozenset({Items.Bow, Items.BombBag})))

    graph.connect(Scene.MountainVillage, Scene.PathToGoronVillage, walk)
    graph.connect(Scene.MountainVillage, Scene.PathToSnowhead, walk)
    graph.connect(Scene.PathToGoronVillage, Scene.GoronVillage, walk)
    graph.connect(Scene.PathToGoronVillage, Scene.GoronRacetrack, walk)
    graph.connect(Scene.GoronVillage, Scene.GoronShrine, walk)
    graph.connect(Scene.GoronVillage, Scene.LonePeakShrine, walk)
    graph.connect(Scene.PathToSnowhead, Scene.Snowhead, walk)

    # Snowhead Temple entrance — gated by Goron Lullaby
    graph.connect(Scene.Snowhead, Scene.SnowheadTemple,
                  Strat("Goron Lullaby", cost=30,
                        requires=frozenset({Masks.Goron, Songs.Lullaby})))
