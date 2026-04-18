from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks

walk = Strat("Walk", cost=30)

def register(graph: GameGraph):
    graph.node(Scene.SouthernSwamp, owl_statue=True)

    graph.node(Scene.SouthernSwamp).check(Songs.Soaring, requires={Items.Ocarina})
    graph.node(Scene.SouthernSwamp).check(Items.Bottle, requires={Masks.Deku})

    # Upgrades
    graph.node(Scene.SouthernSwamp).check(Items.Quiver50, requires={Items.Bow, Items.Quiver40})

    graph.connect(Scene.SouthernSwamp, Scene.DekuPalace, walk)
    graph.connect(Scene.SouthernSwamp, Scene.Woodfall, walk)
    graph.connect(Scene.SouthernSwamp, Scene.WoodsOfMystery, walk)
    graph.connect(Scene.SouthernSwamp, Scene.HagsPotionShop, walk)
    graph.connect(Scene.SouthernSwamp, Scene.SwampSpiderHouse, walk)
