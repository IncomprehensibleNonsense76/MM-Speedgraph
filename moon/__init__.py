from __future__ import annotations
from core import GameGraph

def register(graph: GameGraph):
    from moon import the_moon
    the_moon.register(graph)
