from __future__ import annotations
from core import GameGraph

def register(graph: GameGraph):
    from snowhead import (
        path_to_mountain_village, mountain_village,
        path_to_goron_village, goron_village,
        goron_shrine, goron_racetrack, lone_peak_shrine,
        path_to_snowhead, snowhead,
    )
    path_to_mountain_village.register(graph)
    mountain_village.register(graph)
    path_to_goron_village.register(graph)
    goron_village.register(graph)
    goron_shrine.register(graph)
    goron_racetrack.register(graph)
    lone_peak_shrine.register(graph)
    path_to_snowhead.register(graph)
    snowhead.register(graph)
