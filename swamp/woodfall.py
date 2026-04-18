from __future__ import annotations
from core import GameGraph
from enums import Scene, Items, Remains

def register(graph: GameGraph):
    graph.node(Scene.Woodfall, owl_statue=True)
    graph.node(Scene.Woodfall).check(Items.SpinAttack, requires={Remains.Odolwa})
