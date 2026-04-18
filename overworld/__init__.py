from __future__ import annotations
from core import GameGraph

def register(graph: GameGraph):
    from overworld import termina_field
    termina_field.register(graph)
