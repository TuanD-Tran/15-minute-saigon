import heapq


def multi_source_dijkstra(adj, sources: dict, cutoff_s: float) -> dict:
    dist = {}
    heap = []

    for node, start in sources.items():
        if start <= cutoff_s and start < dist.get(node, float("inf")):
            dist[node] = start
            heap.append((start, node))

    heapq.heapify(heap)
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, float("inf")):
            continue

        for v, w in adj.get(u, ()):
            nd = d + w

            if nd <= cutoff_s and nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return dist
