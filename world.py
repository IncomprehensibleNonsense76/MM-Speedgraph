import heapq
from collections import defaultdict
from enums import Scene as S


DEFAULT_WEIGHT = 30   # seconds per scene transition
TF_WEIGHT = 45        # Termina Field crossings
SOS_COST = 15         # Song of Soaring warp

# Bidirectional connections: (scene_a, scene_b) or (scene_a, scene_b, weight_override)
EDGES = [
    # === Clock Town internal ===
    (S.SouthClockTown, S.NorthClockTown),
    (S.SouthClockTown, S.EastClockTown),
    (S.SouthClockTown, S.WestClockTown),
    (S.SouthClockTown, S.LaundryPool),
    (S.SouthClockTown, S.ClockTowerInterior),
    (S.NorthClockTown, S.EastClockTown),
    (S.NorthClockTown, S.CTGreatFairyFountain),
    (S.ClockTowerInterior, S.ClockTowerRooftop),
    (S.EastClockTown, S.Observatory),

    # === Clock Town <-> Overworld ===
    (S.SouthClockTown, S.TerminaField),

    # === Termina Field exits ===
    (S.TerminaField, S.SouthernSwamp, 180),
    (S.TerminaField, S.PathToMountainVillage),
    (S.TerminaField, S.GreatBayCoast),
    (S.TerminaField, S.MilkRoad),
    (S.TerminaField, S.IkanaTrail),

    # === Southern Swamp area ===
    (S.SouthernSwamp, S.DekuPalace),
    (S.SouthernSwamp, S.Woodfall),
    (S.SouthernSwamp, S.WoodsOfMystery),
    (S.SouthernSwamp, S.HagsPotionShop),
    (S.SouthernSwamp, S.SwampSpiderHouse),
    # NOTE: Woodfall -> WFT edge is handled by dungeon room expansion
    (S.DekuPrincessPrison, S.Woodfall),

    # === Mountain / Snowhead ===
    (S.PathToMountainVillage, S.MountainVillage),
    (S.MountainVillage, S.PathToGoronVillage),
    (S.MountainVillage, S.PathToSnowhead),
    (S.PathToGoronVillage, S.GoronVillage),
    (S.PathToGoronVillage, S.GoronRacetrack),
    (S.GoronVillage, S.GoronShrine),
    (S.GoronVillage, S.LonePeakShrine),
    (S.PathToSnowhead, S.Snowhead),
    (S.Snowhead, S.SnowheadTemple),

    # === Milk Road / Ranch ===
    (S.MilkRoad, S.RomaniRanch),
    (S.MilkRoad, S.GormanTrack),

    # === Great Bay ===
    (S.GreatBayCoast, S.PiratesFortress),
    (S.GreatBayCoast, S.MarineResearchLab),
    (S.GreatBayCoast, S.ZoraCape),
    (S.ZoraCape, S.GreatBayTemple),

    # === Great Bay (other) ===
    (S.GreatBayCoast, S.PinnacleRock),
    (S.GreatBayCoast, S.OceanSpiderHouse),

    # === Ikana ===
    (S.IkanaTrail, S.IkanaCanyon),
    (S.IkanaCanyon, S.IkanaGraveyard),
    (S.IkanaCanyon, S.BeneathTheWell),
    (S.BeneathTheWell, S.IkanaCastle),
    (S.IkanaCanyon, S.StoneTower),
    (S.StoneTower, S.StoneTowerTemple),

    # === Special ===
    (S.ClockTowerRooftop, S.TheMoon, 600),
]


# Scenes that have owl statues
OWL_SCENES = {
    S.SouthClockTown,
    S.SouthernSwamp,
    S.Woodfall,
    S.MountainVillage,
    S.Snowhead,
    S.MilkRoad,
    S.GreatBayCoast,
    S.ZoraCape,
    S.IkanaCanyon,
    S.StoneTower,
}


def _edge_weight(a, b, explicit=None):
    if explicit is not None:
        return explicit
    if a == S.TerminaField or b == S.TerminaField:
        return TF_WEIGHT
    return DEFAULT_WEIGHT


class World:
    def __init__(self, edges=None, dungeons=None):
        if edges is None:
            edges = EDGES
        # adj[node][neighbor] = list of (weight, requires_frozenset_or_None)
        self.adj: dict[str, dict[str, list[tuple[int, frozenset | None]]]] = defaultdict(
            lambda: defaultdict(list)
        )

        # Add scene-level edges (bidirectional, no requirements)
        for edge in edges:
            a, b = edge[0], edge[1]
            w = _edge_weight(a, b, edge[2] if len(edge) > 2 else None)
            self.adj[a][b].append((w, None))
            self.adj[b][a].append((w, None))

        # Expand dungeon room graphs
        if dungeons is None:
            from dungeons import ALL_DUNGEONS, expand_dungeon
            dungeons = ALL_DUNGEONS
        for dungeon in dungeons:
            from dungeons import expand_dungeon
            room_edges, entry_node = expand_dungeon(dungeon)
            for edge in room_edges:
                a, b, w, req = edge
                req_frozen = frozenset(req) if req else None
                self.adj[a][b].append((w, req_frozen))

        self.nodes = set(self.adj.keys())

    def dijkstra(self, start: str, acquired: frozenset[str] | None = None) -> dict[str, int]:
        """Shortest path distances from start, respecting edge requirements."""
        dist = {start: 0}
        heap = [(0, start)]
        while heap:
            d, node = heapq.heappop(heap)
            if d > dist.get(node, float("inf")):
                continue
            for neighbor, edge_options in self.adj[node].items():
                for weight, req in edge_options:
                    if req and (acquired is None or not req <= acquired):
                        continue
                    nd = d + weight
                    if nd < dist.get(neighbor, float("inf")):
                        dist[neighbor] = nd
                        heapq.heappush(heap, (nd, neighbor))
        return dist

    def distance(self, a: str, b: str, acquired: frozenset[str] | None = None) -> int | None:
        if a == b:
            return 0
        return self.dijkstra(a, acquired).get(b)

    def path(self, start: str, end: str, acquired: frozenset[str] | None = None) -> list[str] | None:
        """Shortest weighted path respecting requirements."""
        if start == end:
            return [start]
        dist = {start: 0}
        prev = {start: None}
        heap = [(0, start)]
        while heap:
            d, node = heapq.heappop(heap)
            if node == end:
                result = []
                cur = end
                while cur is not None:
                    result.append(cur)
                    cur = prev[cur]
                return list(reversed(result))
            if d > dist.get(node, float("inf")):
                continue
            for neighbor, edge_options in self.adj[node].items():
                for weight, req in edge_options:
                    if req and (acquired is None or not req <= acquired):
                        continue
                    nd = d + weight
                    if nd < dist.get(neighbor, float("inf")):
                        dist[neighbor] = nd
                        prev[neighbor] = node
                        heapq.heappush(heap, (nd, neighbor))
        return None
