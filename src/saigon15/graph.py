import json
from pathlib import Path

from saigon15.config import WALK_SPEED_MPS
from saigon15.geo import haversine_m

EXCLUDED_HIGHWAYS = {"motorway", "motorway_link", "proposed", "construction", "raceway"}


def walkable(tags: dict) -> bool:
    if tags.get("highway") in EXCLUDED_HIGHWAYS:
        return False

    return tags.get("foot") != "no" and tags.get("access") != "private"


def build_walk_graph(path: str = "data/raw/roads.json"):
    elements = json.loads(Path(path).read_text(encoding="utf-8"))["elements"]
    adj: dict[int, list[tuple[int, float]]] = {}
    coords: dict[int, tuple[float, float]] = {}
    for el in elements:
        if el["type"] != "way" or not walkable(el.get("tags", {})):
            continue

        nodes, geom = el["nodes"], el["geometry"]
        for node, g in zip(nodes, geom):
            if g:
                coords[node] = (g["lat"], g["lon"])

        for i in range(len(nodes) - 1):
            if geom[i] is None or geom[i + 1] is None:
                continue

            a, b = nodes[i], nodes[i + 1]
            seconds = haversine_m(*coords[a], *coords[b]) / WALK_SPEED_MPS
            adj.setdefault(a, []).append((b, seconds))
            adj.setdefault(b, []).append((a, seconds))

    return adj, coords
