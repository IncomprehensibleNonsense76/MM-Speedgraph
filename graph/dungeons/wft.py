"""Woodfall Temple — 11 rooms with room-level routing.

Room 0:  Pre-boss (water, dragonflies)
Room 1:  Main hub lower (spinning wood)
Room 1F: Main hub upper (reached via JS recoil from Room 10)
Room 2:  Entrance hall
Room 3:  Left side (torch puzzle, locked door)
Room 4:  Compass room (off Room 3)
Room 5:  Right side lower (small key)
Room 5F: Right side upper (entered from Room 1F)
Room 6:  Turtles (dungeon map, off Room 5)
Room 7:  Bow chest (upper right)
Room 8:  Frog fight / boss key
Room 9:  Dark room (boes, torches)
Room 10: Top room (dragonflies)
Boss:    Odolwa arena
"""

from __future__ import annotations
from core import GameGraph, Strat, Technique, Ruleset
from enums import Scene, Items, Masks, Remains


def _room(num: int | str) -> str:
    return f"{Scene.WoodfallTemple}:Room{num}"


SK1 = f"{Scene.WoodfallTemple}:SK1"

# Techniques used in WFT strats
isg_bomb = Technique("ISG (Bomb)", consumes={"bombs": 1}, ruleset=Ruleset.NMG)
mega_flip = Technique("Mega Flip", consumes={"bombs": 1}, ruleset=Ruleset.NMG)


def register(graph: GameGraph):
    # === Room nodes ===
    for room in [0, 1, "1F", 2, 3, 4, 5, "5F", 6, 7, 8, 9, 10, "Boss"]:
        graph.node(_room(room))

    # === Checks ===
    graph.node(_room(5)).check(SK1, requires={Masks.Deku, Items.Magic, Items.Ocarina})
    graph.node(_room(7)).check(Items.Bow, requires={SK1})
    graph.node(_room(8)).check(Items.BossKeyWFT, requires={Items.Bow})
    graph.node(_room("Boss")).check(
        Remains.Odolwa, requires={Items.BossKeyWFT},
        duration=180, warp_to=Scene.DekuPrincessPrison)

    # === Overworld connection ===
    graph.connect(Scene.Woodfall, _room(2), Strat("Enter WFT", cost=30))

    # === Room traversals ===

    # Entrance to hub
    graph.connect(_room(2), _room(1),
                  Strat("Deku Launch", cost=20, requires=frozenset({Masks.Deku})))
    graph.connect(_room(2), _room(1),
                  Strat("Hookshot", cost=10, requires=frozenset({Items.Hookshot})))

    # Right side (lower)
    graph.connect(_room(1), _room(5), Strat("Walk", cost=15))
    graph.connect(_room(5), _room(6),
                  Strat("Deku Lower Path", cost=20, requires=frozenset({Masks.Deku})))

    # Left side (locked door from hub)
    graph.connect(_room(1), _room(3),
                  Strat("Small Key Door", cost=15, requires=frozenset({SK1})))
    graph.connect(_room(3), _room(4),
                  Strat("Light Torch", cost=20, requires=frozenset({Items.BombBag})))
    graph.connect(_room(3), _room(9), Strat("Walk", cost=20))
    graph.connect(_room(9), _room(10), Strat("Walk", cost=20))

    # Room 10 to upper hub (one-way)
    graph.connect(_room(10), _room("1F"),
                  Strat("JS Recoil", cost=10, oneway=True,
                        requires=frozenset({Masks.Deku, Items.Bow})))
    graph.connect(_room(10), _room("1F"),
                  Strat("Deku Flight", cost=30, oneway=True,
                        requires=frozenset({Masks.Deku})))

    # Upper path
    graph.connect(_room("1F"), _room("5F"), Strat("Walk", cost=15))
    graph.connect(_room("5F"), _room(7), Strat("Walk", cost=15))
    graph.connect(_room(7), _room(8),
                  Strat("Eye Switch", cost=25, requires=frozenset({Items.Bow})))

    # Pre-boss (light torch in hub with arrow)
    graph.connect(_room(1), _room(0),
                  Strat("Light Torch (Bow)", cost=20, requires=frozenset({Items.Bow})))
    graph.connect(_room(1), _room(0),
                  Strat("Light Torch (Fire)", cost=20, requires=frozenset({Items.FireArrows})))

    # Boss door — same connection, different strats
    graph.connect(_room(0), _room("Boss"),
                  Strat("Hookshot Cross", cost=15, requires=frozenset({Items.Hookshot})))
    graph.connect(_room(0), _room("Boss"),
                  Strat("Deku + Bow", cost=45, requires=frozenset({Masks.Deku, Items.Bow})))

    # === NMG Strats ===
    # Torch Mega — skip left side entirely
    graph.connect(_room(1), _room("1F"),
                  Strat("Torch Mega", cost=25, techniques=[isg_bomb, mega_flip]))
