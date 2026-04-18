from __future__ import annotations
from core import GameGraph

def register(graph: GameGraph):
    from milk_road import milk_road_scene, romani_ranch, gorman_track
    milk_road_scene.register(graph)
    romani_ranch.register(graph)
    gorman_track.register(graph)
