from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks, Remains

walk = Strat("Walk", cost=30)


def register(graph: GameGraph):
    graph.node(Scene.SouthernSwamp, owl_statue=True)
    graph.node(Scene.DekuPalace)
    graph.node(Scene.Woodfall, owl_statue=True)
    graph.node(Scene.WoodsOfMystery)
    graph.node(Scene.HagsPotionShop)
    graph.node(Scene.SwampSpiderHouse)
    graph.node(Scene.DekuPrincessPrison)
    graph.node(Scene.GiantsChamber)

    # === Checks ===
    graph.node(Scene.SouthernSwamp).check(Songs.Soaring, requires={Items.Ocarina})
    graph.node(Scene.SouthernSwamp).check(Items.Bottle, requires={Masks.Deku})
    graph.node(Scene.DekuPalace).check(Items.MagicBeans)
    graph.node(Scene.DekuPalace).check(Songs.Sonata, requires={Masks.Deku})
    graph.node(Scene.DekuPrincessPrison).check(
        Songs.OathToOrder, requires={Remains.Odolwa})
    graph.node(Scene.DekuPrincessPrison).check(
        Items.DekuPrincess, requires={Remains.Odolwa, Items.Bottle})
    graph.node(Scene.DekuPalace).check(
        Masks.Scents, requires={Items.DekuPrincess, Masks.Deku})
    graph.node(Scene.SwampSpiderHouse).check(
        Masks.Truth, requires={Masks.Deku, Items.Bottle, Items.Bow})
    graph.node(Scene.Woodfall).check(Items.SpinAttack, requires={Remains.Odolwa})

    # === Traversals ===
    graph.connect(Scene.SouthernSwamp, Scene.DekuPalace, walk)
    graph.connect(Scene.SouthernSwamp, Scene.Woodfall, walk)
    graph.connect(Scene.SouthernSwamp, Scene.WoodsOfMystery, walk)
    graph.connect(Scene.SouthernSwamp, Scene.HagsPotionShop, walk)
    graph.connect(Scene.SouthernSwamp, Scene.SwampSpiderHouse, walk)
    graph.connect(Scene.DekuPrincessPrison, Scene.Woodfall, walk)
