"""Stone Tower Temple — scene-level placeholder until room routing is added."""

from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks, Remains


def register(graph: GameGraph):
    graph.node(Scene.StoneTowerTemple)

    graph.node(Scene.StoneTowerTemple).check(
        Items.LightArrows, requires={Songs.Elegy, Masks.Goron, Masks.Zora, Masks.Deku})
    graph.node(Scene.StoneTowerTemple).check(
        Masks.Giant, requires={Items.LightArrows})
    graph.node(Scene.StoneTowerTemple).check(
        Items.BossKeySTT, requires={Items.LightArrows})
    graph.node(Scene.StoneTowerTemple).check(
        Remains.Twinmold, requires={Items.BossKeySTT, Masks.Giant},
        duration=120, warp_to=Scene.IkanaCanyon)
