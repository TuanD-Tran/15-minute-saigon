import random

import networkx as nx

from saigon15.dijkstra import multi_source_dijkstra

# A -- 100 -- B -- 100 -- C -- 100 -- D
LINE = {
    "A": [("B", 100)],
    "B": [("A", 100), ("C", 100)],
    "C": [("B", 100), ("D", 100)],
    "D": [("C", 100)],
}


def test_single_source_with_cutoff():
    dist = multi_source_dijkstra(LINE, {"A": 0.0}, 250)
    assert dist == {"A": 0.0, "B": 100, "C": 200}


def test_two_sources_take_the_nearest():
    dist = multi_source_dijkstra(LINE, {"A": 0.0, "D": 0.0}, 250)
    assert dist == {"A": 0.0, "B": 100, "C": 100, "D": 0.0}


def test_matches_networkx_on_random_graph():
    rng = random.Random(0)
    graph = nx.gnm_random_graph(60, 150, seed=1)
    adj = {u: [] for u in graph}
    for u, v in graph.edges:
        w = rng.uniform(10, 300)
        graph[u][v]["w"] = w
        adj[u].append((v, w))
        adj[v].append((u, w))
    sources = {0: 0.0, 5: 0.0, 9: 0.0}
    mine = multi_source_dijkstra(adj, sources, 600)
    ref = nx.multi_source_dijkstra_path_length(graph, set(sources), cutoff=600, weight="w")
    assert mine.keys() == ref.keys()
    assert all(abs(mine[k] - ref[k]) < 1e-9 for k in mine)
