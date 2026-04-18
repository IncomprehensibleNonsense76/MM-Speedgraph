from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks, Remains, TimeSlot

walk = Strat("Walk", cost=30)


def register(graph: GameGraph):
    graph.node(Scene.GreatBayCoast, owl_statue=True)
    graph.node(Scene.PiratesFortress)
    graph.node(Scene.MarineResearchLab)
    graph.node(Scene.ZoraCape, owl_statue=True)
    graph.node(Scene.PinnacleRock)
    graph.node(Scene.OceanSpiderHouse)

    # === Checks ===
    graph.node(Scene.GreatBayCoast).check(
        Masks.Zora, requires={Songs.Healing}, duration=90)
    graph.node(Scene.PiratesFortress).check(
        Items.Hookshot, requires={Masks.Zora, Masks.Goron})
    graph.node(Scene.MarineResearchLab).check(
        Songs.NewWave,
        requires={Masks.Zora, Items.Hookshot, Items.Bottle, Items.BottleAliens, Items.BottleGoldDust})
    graph.node(Scene.ZoraCape).check(Items.EnhancedDefense, requires={Remains.Gyorg})
    graph.node(Scene.ZoraCape).check(
        Items.BottleBeaver, requires={Masks.Zora, Items.Hookshot})
    graph.node(Scene.OceanSpiderHouse).check(
        Items.GiantWallet, requires={Items.Epona},
        time=frozenset({TimeSlot.DAY_1}))

    # === Traversals ===
    # PF — need Zora to swim there
    graph.connect(Scene.GreatBayCoast, Scene.PiratesFortress,
                  Strat("Zora Swim", cost=30, requires=frozenset({Masks.Zora})))
    graph.connect(Scene.GreatBayCoast, Scene.MarineResearchLab, walk)
    graph.connect(Scene.GreatBayCoast, Scene.ZoraCape, walk)
    graph.connect(Scene.GreatBayCoast, Scene.PinnacleRock, walk)
    graph.connect(Scene.GreatBayCoast, Scene.OceanSpiderHouse, walk)

    # GBT — need turtle ride from New Wave
    graph.connect(Scene.ZoraCape, Scene.GreatBayTemple,
                  Strat("Turtle Ride", cost=30, requires=frozenset({Songs.NewWave})))
