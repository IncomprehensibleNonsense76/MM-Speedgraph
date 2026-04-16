from collections import deque, defaultdict
from enums import Scene as S


# Bidirectional loading zone connections between adjacent scenes
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
    (S.TerminaField, S.SouthernSwamp),
    (S.TerminaField, S.PathToMountainVillage),
    (S.TerminaField, S.GreatBayCoast),
    (S.TerminaField, S.MilkRoad),
    (S.TerminaField, S.IkanaTrail),

    # === Southern Swamp area ===
    (S.SouthernSwamp, S.DekuPalace),
    (S.SouthernSwamp, S.Woodfall),
    (S.SouthernSwamp, S.WoodsOfMystery),
    (S.SouthernSwamp, S.HagsPotionShop),
    (S.Woodfall, S.WoodfallTemple),
    (S.SouthernSwamp, S.SwampSpiderHouse),

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
    (S.ClockTowerRooftop, S.TheMoon),
]


# Scenes that have owl statues (activatable with human + sword)
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


class World:
    def __init__(self, edges=None):
        if edges is None:
            edges = EDGES
        self.adj: dict[str, set[str]] = defaultdict(set)
        for a, b in edges:
            self.adj[a].add(b)
            self.adj[b].add(a)
        self.nodes = set(self.adj.keys())

    def bfs(self, start: str) -> dict[str, int]:
        """BFS from start, returns {node: distance}."""
        dist = {start: 0}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in self.adj[node]:
                if neighbor not in dist:
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)
        return dist

    def distance(self, a: str, b: str) -> int | None:
        """Shortest path length from a to b, or None if unreachable."""
        if a == b:
            return 0
        return self.bfs(a).get(b)

    def all_pairs(self) -> dict[tuple[str, str], int]:
        """All-pairs shortest path distances."""
        result = {}
        for node in self.nodes:
            for dest, d in self.bfs(node).items():
                result[(node, dest)] = d
        return result

    def path(self, start: str, end: str) -> list[str] | None:
        """Return the actual shortest path as a list of scene names."""
        if start == end:
            return [start]
        prev = {start: None}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            if node == end:
                result = []
                cur = end
                while cur is not None:
                    result.append(cur)
                    cur = prev[cur]
                return list(reversed(result))
            for neighbor in self.adj[node]:
                if neighbor not in prev:
                    prev[neighbor] = node
                    queue.append(neighbor)
        return None
