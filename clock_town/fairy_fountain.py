from __future__ import annotations
from core import GameGraph
from enums import Scene, Items, Masks

def register(graph: GameGraph):
    graph.node(Scene.CTGreatFairyFountain)

    graph.node(Scene.CTGreatFairyFountain).check(Items.Magic, requires={Items.StrayFairyCT})
    graph.node(Scene.CTGreatFairyFountain).check(Masks.GreatFairy, requires={Items.Magic, Masks.Deku})
