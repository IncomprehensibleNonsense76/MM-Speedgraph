from __future__ import annotations
from core import GameGraph
from enums import Scene, Items, Songs, Masks, TimeSlot

def register(graph: GameGraph):
    graph.node(Scene.IkanaGraveyard)

    graph.node(Scene.IkanaGraveyard).check(Masks.Captain, requires={Songs.Sonata})
    graph.node(Scene.IkanaGraveyard).check(Songs.Storms, requires={Masks.Captain})
    graph.node(Scene.IkanaGraveyard).check(
        Items.BottleGraveyard, requires={Items.Bow, Masks.Captain},
        time=frozenset({TimeSlot.NIGHT_3}))
