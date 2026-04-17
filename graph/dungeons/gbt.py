"""Great Bay Temple — scene-level placeholder until room routing is added."""

from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks, Remains


def register(graph: GameGraph):
    graph.node(Scene.GreatBayTemple)

    graph.node(Scene.GreatBayTemple).check(
        Items.IceArrows, requires={Songs.NewWave, Masks.Zora})
    graph.node(Scene.GreatBayTemple).check(
        Items.BossKeyGBT, requires={Items.IceArrows})
    graph.node(Scene.GreatBayTemple).check(
        Remains.Gyorg, requires={Items.BossKeyGBT},
        duration=120, warp_to=Scene.ZoraCape)
