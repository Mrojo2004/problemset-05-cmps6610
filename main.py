from collections import deque
from heapq import heappush, heappop 

def shortest_shortest_path(graph, source):
    """
    Params: 
      graph.....a graph represented as a dict where each key is a vertex
                and the value is a set of (vertex, weight) tuples (as in the test case)
      source....the source node
      
    Returns:
      a dict where each key is a vertex and the value is a tuple of
      (shortest path weight, shortest path number of edges). See test case for example.
    """
    # Dijkstra where priorities are (weight, num_edges) tuples. Tuples compare lexicographically, meaning that ties in weight are broken by fewer edges.
    result = {}
    frontier = [(0, 0, source)]
    while frontier:
        dist, num_edges, v = heappop(frontier)
        if v in result:
            continue
        result[v] = (dist, num_edges)
        for neighbor, weight in graph.get(v, ()):
            if neighbor not in result:
                heappush(frontier, (dist + weight, num_edges + 1, neighbor))
    return result
    
