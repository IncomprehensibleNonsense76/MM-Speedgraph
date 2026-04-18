from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Masks

def register(graph: GameGraph):
    graph.node(Scene.SouthClockTown, owl_statue=True)

    # Edges to other Clock Town areas
    walk = Strat("Walk", cost=30)
    graph.connect(Scene.SouthClockTown, Scene.NorthClockTown, walk)
    graph.connect(Scene.SouthClockTown, Scene.EastClockTown, walk)
    graph.connect(Scene.SouthClockTown, Scene.WestClockTown, walk)
    graph.connect(Scene.SouthClockTown, Scene.LaundryPool, walk)
    graph.connect(Scene.SouthClockTown, Scene.ClockTowerInterior, walk)

    # To overworld
    graph.connect(Scene.SouthClockTown, Scene.TerminaField, Strat("Walk", cost=30))

    # Clock Tower Rooftop: one-way from SCT at midnight Night 3
    graph.connect(Scene.SouthClockTown, Scene.ClockTowerRooftop,
                  Strat("Midnight Climb", cost=30, oneway=True))
