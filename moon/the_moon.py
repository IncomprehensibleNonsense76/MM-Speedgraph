from __future__ import annotations
from core import GameGraph, Strat
from enums import Scene, Items, Songs, Masks, Remains, Events, TimeSlot

def register(graph: GameGraph):
    graph.node(Scene.TheMoon)

    # Enter Moon check is on ClockTowerRooftop (registered by clock_tower.py)
    graph.node(Scene.ClockTowerRooftop).check(
        Events.EnterMoon,
        requires={Remains.Odolwa, Remains.Goht, Remains.Gyorg, Remains.Twinmold,
                  Songs.OathToOrder, Items.Ocarina},
        time=frozenset({TimeSlot.NIGHT_3}))

    graph.node(Scene.TheMoon).check(Events.KillMajora, requires={Events.EnterMoon})

    # Fierce Deity
    graph.node(Scene.TheMoon).check(
        Masks.FierceDeity,
        requires={
            Masks.GreatFairy, Masks.Blast, Masks.Stone, Masks.Bremen, Masks.Kamaro,
            Masks.KafeiMask, Masks.AllNight, Masks.BunnyHood, Masks.DonGero,
            Masks.Scents, Masks.Truth, Masks.Captain, Masks.Garo, Masks.Gibdo,
            Masks.Romani, Masks.CircusLeader, Masks.Giant,
            Masks.Keaton, Masks.Postman, Masks.Couple, Events.EnterMoon})

    graph.connect(Scene.ClockTowerRooftop, Scene.TheMoon,
                  Strat("Moon Cutscene", cost=600, oneway=True))
