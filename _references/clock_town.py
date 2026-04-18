from __future__ import annotations
from core import GameGraph, Strat, Ruleset
from enums import Scene, Items, Songs, Masks, TimeSlot

# Time slot shorthand
N1 = frozenset({TimeSlot.NIGHT_1})
N3 = frozenset({TimeSlot.NIGHT_3})
ANY_NIGHT = frozenset({TimeSlot.NIGHT_1, TimeSlot.NIGHT_2, TimeSlot.NIGHT_3})


def register(graph: GameGraph):
    # === Nodes ===
    graph.node(Scene.SouthClockTown, owl_statue=True)
    graph.node(Scene.NorthClockTown)
    graph.node(Scene.EastClockTown)
    graph.node(Scene.WestClockTown)
    graph.node(Scene.LaundryPool)
    graph.node(Scene.ClockTowerInterior)
    graph.node(Scene.ClockTowerRooftop)
    graph.node(Scene.CTGreatFairyFountain)
    graph.node(Scene.Observatory)

    # === Checks ===
    graph.node(Scene.LaundryPool).check(Items.StrayFairyCT)
    graph.node(Scene.CTGreatFairyFountain).check(Items.Magic, requires={Items.StrayFairyCT})
    graph.node(Scene.ClockTowerRooftop).check(Items.Ocarina, requires={Items.Magic}, time=N3)
    graph.node(Scene.ClockTowerRooftop).check(Songs.Time, requires={Items.Ocarina}, time=N3)
    graph.node(Scene.ClockTowerInterior).check(Songs.Healing, requires={Items.Ocarina, Songs.Time})
    graph.node(Scene.ClockTowerInterior).check(Masks.Deku, requires={Songs.Healing})
    graph.node(Scene.WestClockTown).check(Items.BombBag)
    graph.node(Scene.CTGreatFairyFountain).check(Masks.GreatFairy, requires={Items.Magic, Masks.Deku})
    graph.node(Scene.NorthClockTown).check(Masks.Blast, requires={Masks.Deku}, time=N1)
    graph.node(Scene.EastClockTown).check(Masks.KafeiMask, requires={Masks.Deku})
    graph.node(Scene.LaundryPool).check(Masks.Bremen, requires={Masks.Deku}, time=ANY_NIGHT)
    graph.node(Scene.WestClockTown).check(Masks.AllNight, requires={Masks.Blast}, time=N3)
    graph.node(Scene.WestClockTown).check(Items.AdultWallet)
    graph.node(Scene.EastClockTown).check(Items.BombersNotebook, requires={Masks.Deku, Items.Magic})
    graph.node(Scene.Observatory).check(Items.MoonsTear, requires={Items.Magic})
    graph.node(Scene.EastClockTown).check(Items.RoomKey, requires={Masks.Deku})

    # === Traversals ===
    walk = Strat("Walk", cost=30)

    graph.connect(Scene.SouthClockTown, Scene.NorthClockTown, walk)
    graph.connect(Scene.SouthClockTown, Scene.EastClockTown, walk)
    graph.connect(Scene.SouthClockTown, Scene.WestClockTown, walk)
    graph.connect(Scene.SouthClockTown, Scene.LaundryPool, walk)
    graph.connect(Scene.SouthClockTown, Scene.ClockTowerInterior, walk)
    graph.connect(Scene.NorthClockTown, Scene.EastClockTown, walk)
    graph.connect(Scene.NorthClockTown, Scene.CTGreatFairyFountain, walk)
    # Clock Tower Rooftop: accessed from SCT at midnight Night 3, one-way (exits: SoT or Oath)
    graph.connect(Scene.SouthClockTown, Scene.ClockTowerRooftop,
                  Strat("Midnight Climb", cost=30, oneway=True))
    graph.connect(Scene.EastClockTown, Scene.Observatory, walk)
