"""Snowhead Temple — scene-level placeholder until room routing is added."""

from __future__ import annotations
from core import GameGraph, Strat, Technique, Ruleset
from core import Version
from enums import Scene, Items, Songs, Masks, Remains

# NMG techniques
isg_bomb = Technique("ISG (Bomb)", consumes={"bombs": 1}, ruleset=Ruleset.NMG)
hess = Technique("HESS", ruleset=Ruleset.NMG)


def register(graph: GameGraph):
    graph.node(Scene.SnowheadTemple)

    # === Checks ===
    graph.node(Scene.SnowheadTemple).check(
        Items.FireArrows, requires={Songs.Lullaby, Masks.Goron, Items.Magic})
    graph.node(Scene.SnowheadTemple).check(
        Items.BossKeySHT, requires={Items.FireArrows})
    graph.node(Scene.SnowheadTemple).check(
        Remains.Goht, requires={Items.BossKeySHT},
        duration=120, warp_to=Scene.MountainVillage)

    # === NMG: Snowhead HESS (skip Lullaby requirement on entrance) ===
    graph.connect(Scene.Snowhead, Scene.SnowheadTemple,
                  Strat("Snowhead HESS (Bomb)", cost=90,
                        techniques=[isg_bomb, hess],
                        versions=frozenset({Version.EN})))
