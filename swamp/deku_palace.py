from __future__ import annotations
from core import GameGraph
from enums import Scene, Items, Songs, Masks

def register(graph: GameGraph):
    graph.node(Scene.DekuPalace)

    graph.node(Scene.DekuPalace).check(Items.MagicBeans)
    graph.node(Scene.DekuPalace).check(Songs.Sonata, requires={Masks.Deku})
    graph.node(Scene.DekuPalace).check(Masks.Scents, requires={Items.DekuPrincess, Masks.Deku})
