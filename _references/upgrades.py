"""Upgrades — bomb bags, quivers, wallets, swords, bottles, circus leader."""

from __future__ import annotations
from core import GameGraph
from enums import Scene, Items, Masks, Songs, Remains, TimeSlot

ANY_NIGHT = frozenset({TimeSlot.NIGHT_1, TimeSlot.NIGHT_2, TimeSlot.NIGHT_3})


def register(graph: GameGraph):
    # === Bomb Bag upgrades ===
    graph.node(Scene.WestClockTown).check(
        Items.BombBag30, requires={Items.BombBag, Masks.Blast})
    graph.node(Scene.MountainVillage).check(
        Items.BombBag40, requires={Items.BombBag30, Masks.Goron})

    # === Quiver upgrades (progressive) ===
    graph.node(Scene.EastClockTown).check(Items.Quiver40, requires={Items.Bow})
    graph.node(Scene.SouthernSwamp).check(
        Items.Quiver50, requires={Items.Bow, Items.Quiver40})

    # === Bottle (Gold Dust) ===
    graph.node(Scene.WestClockTown).check(
        Items.BottleGoldDust, requires={Items.GoldDust}, time=ANY_NIGHT)

    # === Circus Leader's Mask (Milk Bar) ===
    graph.node(Scene.EastClockTown).check(
        Masks.CircusLeader,
        requires={Masks.Romani, Masks.Deku, Masks.Goron, Masks.Zora, Items.Ocarina})
