from saigon15.graph import build_walk_graph

adj, coords = build_walk_graph()
n_edges = sum(len(v) for v in adj.values()) // 2
print("node:", len(adj), "| edge:", n_edges)
degrees = [len(v) for v in adj.values()]
print("Average level:", sum(degrees) / len(degrees))
