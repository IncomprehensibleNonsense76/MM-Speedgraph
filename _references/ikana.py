from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks, Remains, TimeSlot

walk = Strat("Walk", cost=30)
N3 = frozenset({TimeSlot.NIGHT_3})


def register(graph: GameGraph):
    graph.node(Scene.IkanaTrail)
    graph.node(Scene.IkanaCanyon, owl_statue=True)
    graph.node(Scene.IkanaGraveyard)
    graph.node(Scene.BeneathTheWell)
    graph.node(Scene.IkanaCastle)
    graph.node(Scene.StoneTower, owl_statue=True)

    # === Checks ===
    graph.node(Scene.IkanaTrail).check(
        Masks.Stone, requires={Items.LensOfTruth, Items.Bottle})
    graph.node(Scene.IkanaGraveyard).check(
        Masks.Captain, requires={Songs.Sonata})
    graph.node(Scene.IkanaGraveyard).check(
        Songs.Storms, requires={Masks.Captain})
    graph.node(Scene.IkanaGraveyard).check(
        Items.BottleGraveyard, requires={Items.Bow, Masks.Captain}, time=N3)
    graph.node(Scene.IkanaCanyon).check(
        Masks.Gibdo, requires={Songs.Storms, Songs.Healing})
    graph.node(Scene.BeneathTheWell).check(
        Items.MirrorShield,
        requires={Masks.Gibdo, Items.BombBag, Items.Bottle, Items.MagicBeans, Items.Epona})
    graph.node(Scene.IkanaCastle).check(
        Songs.Elegy, requires={Items.MirrorShield, Items.PowderKeg})
    graph.node(Scene.IkanaCanyon).check(
        Items.GreatFairySword, requires={Remains.Twinmold})

    # === Traversals ===
    # Ikana Trail -> Graveyard: Epona or Goron+Bombs (before Garo gate)
    graph.connect(Scene.IkanaTrail, Scene.IkanaGraveyard,
                  Strat("Epona", cost=30, requires=frozenset({Items.Epona})))
    graph.connect(Scene.IkanaTrail, Scene.IkanaGraveyard,
                  Strat("Goron Damage Boost", cost=30,
                        requires=frozenset({Masks.Goron, Items.BombBag})))

    # Ikana Trail -> Canyon: full gate (Garo + Hookshot + access)
    graph.connect(Scene.IkanaTrail, Scene.IkanaCanyon,
                  Strat("Garo + Hookshot + Epona", cost=30,
                        requires=frozenset({Masks.Garo, Items.Hookshot, Items.Epona})))
    graph.connect(Scene.IkanaTrail, Scene.IkanaCanyon,
                  Strat("Garo + Hookshot + Goron Boost", cost=30,
                        requires=frozenset({Masks.Garo, Items.Hookshot, Masks.Goron, Items.BombBag})))

    # Inside Ikana Canyon
    graph.connect(Scene.IkanaCanyon, Scene.IkanaGraveyard, walk)
    graph.connect(Scene.IkanaCanyon, Scene.BeneathTheWell, walk)
    graph.connect(Scene.BeneathTheWell, Scene.IkanaCastle, walk)
    graph.connect(Scene.IkanaCanyon, Scene.StoneTower, walk)

    # Stone Tower Temple — need Elegy + all forms
    graph.connect(Scene.StoneTower, Scene.StoneTowerTemple,
                  Strat("Elegy Statues", cost=30,
                        requires=frozenset({Songs.Elegy, Masks.Goron, Masks.Zora, Masks.Deku})))
