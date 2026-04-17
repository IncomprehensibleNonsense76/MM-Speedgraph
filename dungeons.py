from __future__ import annotations

"""Room-level graph data for dungeons.

Edge format: (from_room, to_room, strats, bidirectional)

strats is either:
  - A single (cost, requires) tuple for one strat
  - A list of (cost, requires) tuples for multiple strats
  - An int for a simple unconditional edge (cost only)

The solver picks the cheapest strat whose requirements are met.
When glitches are added, they're just more strats on the same connections.
"""

from enums import Scene as S, Items as I, Masks as M, Remains as R


def room_node(scene: str, room: int | str) -> str:
    """Generate flat graph node name for a room."""
    return f"{scene}:Room{room}"


def small_key(scene: str, num: int) -> str:
    """Generate ID for a dungeon small key. Keys are numbered per dungeon."""
    return f"{scene}:SK{num}"


def _normalize_strats(strats):
    """Normalize strat formats into a list of (cost, requires_or_None)."""
    if isinstance(strats, int):
        return [(strats, None)]
    if isinstance(strats, tuple) and len(strats) == 2:
        return [strats]
    if isinstance(strats, list):
        return strats
    raise ValueError(f"Invalid strat format: {strats}")


# =============================================================================
# WOODFALL TEMPLE
# =============================================================================
# Room 0:  Pre-boss (water, dragonflies)
# Room 1:  Main hub lower (spinning wood)
# Room 1F: Main hub upper (reached via JS recoil from Room 10)
# Room 2:  Entrance hall
# Room 3:  Left side (torch puzzle, locked door)
# Room 4:  Compass room (off Room 3)
# Room 5:  Right side lower (small key)
# Room 5F: Right side upper (entered from Room 1F)
# Room 6:  Turtles (dungeon map, off Room 5)
# Room 7:  Bow chest (upper right)
# Room 8:  Frog fight / boss key
# Room 9:  Dark room (boes, torches)
# Room 10: Top room (dragonflies)
# Boss:    Odolwa arena (separate scene, two paths from Room 0)

_WFT = S.WoodfallTemple

WFT_SK1 = small_key(_WFT, 1)

WOODFALL_TEMPLE = {
    "scene": _WFT,
    "entry_room": 2,
    "overworld_link": S.Woodfall,
    "overworld_weight": 30,
    "edges": [
        # Entrance to hub
        (2, 1, [(20, {M.Deku}), (10, {I.Hookshot})]),
        # Right side (lower)
        (1, 5, 15),
        (5, 6, (20, {M.Deku})),  # lower path to turtles
        # Left side (locked door from hub)
        (1, 3, (15, {WFT_SK1})),  # needs small key from Room 5
        (3, 4, (20, {I.BombBag})),  # compass room, light torch
        (3, 9, 20),  # dark room
        (9, 10, 20),  # up to top room
        # JS recoil shortcut (one-way)
        # One-way: Room 10 to upper hub
        (
            10,
            "1F",
            [
                (10, {M.Deku, I.Bow}),  # JS recoil (fast, needs weapon)
                (30, {M.Deku}),
            ],  # vanilla deku flight (slow, no weapon)
            False,
        ),
        # Upper path
        ("1F", "5F", 15),  # upper hub to upper right side
        ("5F", 7, 15),  # to bow room
        (7, 8, (25, {I.Bow})),  # eye switch to frog fight
        # Pre-boss (light torch in hub with arrow)
        (1, 0, [(20, {I.Bow}), (20, {I.FireArrows})]),
        # Boss door — same connection, different strats
        (0, "Boss", [(15, {I.Hookshot}), (45, {M.Deku, I.Bow})]),
    ],
}


def expand_dungeon(dungeon: dict):
    """Convert a dungeon definition into flat graph edges.

    Returns:
        edges: list of (node_a, node_b, weight, requires_set_or_None)
        entry_node: the node that connects to the overworld
    """
    scene = dungeon["scene"]
    entry_room = dungeon["entry_room"]
    overworld = dungeon["overworld_link"]
    ow_weight = dungeon.get("overworld_weight", 30)

    edges = []
    entry_node = room_node(scene, entry_room)

    # Overworld <-> entry room
    edges.append((overworld, entry_node, ow_weight, None))

    for edge in dungeon["edges"]:
        from_r, to_r = edge[0], edge[1]
        strats_or_bidir = edge[2]
        from_node = room_node(scene, from_r)
        to_node = room_node(scene, to_r)

        # Detect if last element is a bool (bidirectional flag)
        bidir = True
        if isinstance(edge[-1], bool):
            bidir = edge[-1]
            strats_or_bidir = edge[2] if len(edge) > 3 else edge[2]

        strats = _normalize_strats(strats_or_bidir)

        for cost, req in strats:
            edges.append((from_node, to_node, cost, req))
            if bidir:
                edges.append((to_node, from_node, cost, req))

    return edges, entry_node


# All dungeons — add more as they get mapped
ALL_DUNGEONS = [WOODFALL_TEMPLE]

# TODO: SNOWHEAD_TEMPLE (14 rooms, 7 levels, big open tower...)
# TODO: GREAT_BAY_TEMPLE (16 rooms, pipes and water flow)
# TODO: STONE_TOWER_TEMPLE (12 rooms, flipping mechanic)
