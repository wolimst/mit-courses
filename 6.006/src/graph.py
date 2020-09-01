from __future__ import annotations
from typing import Set, Tuple, List, Dict, Union
import sys
import math


def breadth_first_search(graph: Graph, source: Vertex) -> Dict[Vertex, Vertex]:
    """Breadth-first search. Ignore weights.
    Return parent dictionary, i.e. {vertex: parent vertex}.

    Complexity: O(|V| + |E|)
                where V is vertices and E is edges of the graph.
    """
    parent = {source: None}
    frontiers = [source]
    for frontier in frontiers:
        neighbors = graph.get_neighbors(frontier)
        for neighbor in neighbors:
            if neighbor not in parent:
                parent[neighbor] = frontier
                frontiers.append(neighbor)
    return parent


def depth_first_search(graph: Graph, source: Vertex) -> List[Vertex]:
    """Depth-first search. Ignore weights.
    Return visited vertices ordered by dead-end reached time.

    Complexity: O(|V| + |E|)
                where V is vertices and E is edges of the graph.
    """

    def dfs_subroutine(vertex: Vertex):
        neighbors = graph.get_neighbors(vertex)
        for neighbor in neighbors:
            if neighbor not in parent:
                parent[neighbor] = vertex
                dfs_subroutine(neighbor)
        finished.append(vertex)

    parent = {source: None}
    finished = []
    dfs_subroutine(source)
    return finished


def dijkstra(
    graph, source: Vertex
) -> Tuple[Dict[Vertex, Union[int, float], Dict[Vertex, Vertex]]]:
    """Dijkstra's shortest path algorithm. All edges in the graph should have
    non-negative weight. Complexity can be improved by using a binary min-heap
    or Fibonacci heap which can perform 'extract-min' and 'decrease-key'
    efficiently.

    Return (distance, parent)
           where `distance` and `parent` are dictionaries,
           i.e. distance = {v: distance from the source} for v ∈ V,
                parent = {v: parent vertex} for reachable v ∈ V from source.

    Complexity: O(|V|^2 + |E|)
    """
    assert (
        graph.is_non_neg_weight_graph is True
    ), "Graph has edges with negative weight."

    parent = {source: None}
    distance = dict.fromkeys(graph.get_vertices(), math.inf)
    distance[source] = 0
    vertices_to_visit = distance.copy()

    while len(vertices_to_visit) != 0:
        frontier = min(vertices_to_visit, key=vertices_to_visit.get)
        vertices_to_visit.pop(frontier)

        neighbors = graph.get_neighbors(frontier)
        for neighbor in neighbors:
            edge = graph.get_edge(frontier, neighbor)
            new_distance = distance[frontier] + edge.get_weight()
            if distance[neighbor] > new_distance:
                distance[neighbor] = new_distance
                vertices_to_visit[neighbor] = new_distance
                parent[neighbor] = frontier

    return (distance, parent)


def bellman_ford(
    graph: Graph, source: Vertex
) -> Tuple[Dict[Vertex, Union[int, float], Dict[Vertex, Vertex]]]:
    """Bellman-Ford algorithm. Shortest path in a graph with negative weight
    edges can be calculated when there is no negative cycle.
    
    Return (distance, parent)
           where `distance` and `parent` are dictionaries,
           i.e. distance = {v: distance from the source} for v ∈ V,
                parent = {v: parent vertex} for reachable v ∈ V from source.
    
    Raise RuntimeError
          when there are negative cycles reachable from the source.

    Complexity: O(|V|⋅|E|)
    """
    edges = graph.get_edges()
    parent = {source: None}
    distance = dict.fromkeys(graph.get_vertices(), math.inf)
    distance[source] = 0
    for i in range(len(graph.get_vertices()) - 1):
        for edge in edges:
            u, v = edge.get_source(), edge.get_dest()
            new_dist_to_v = distance[u] + edge.get_weight()
            if distance[v] > new_dist_to_v:
                parent[v] = u
                distance[v] = new_dist_to_v

    for edge in edges:
        u, v = edge.get_source(), edge.get_dest()
        if distance[v] > distance[u] + edge.get_weight():
            raise RuntimeError(
                "Graph has negative cycle(s) reachable from source."
            )

    return (distance, parent)


class Graph:
    """Weighted directed graph. Edges are represented by adjacency list."""

    def __init__(self, vertices: Set[Vertex], edges: Tuple[WeightedEdge]):
        self.vertices = set(vertices)
        self.is_non_neg_weight_graph = True
        self.adj_edge_list = {}
        for edge in edges:  # TODO: check duplicate edges
            source = edge.get_source()
            if source in self.adj_edge_list:
                self.adj_edge_list[source].append(edge)
            else:
                self.adj_edge_list[source] = [edge]

            if edge.get_weight() < 0:
                self.is_non_neg_weight_graph = False

        # Check vertices ⊇ vertices from edges
        if not self.vertices.issuperset(self.adj_edge_list.keys()):
            self.vertices.update(self.adj_edge_list.keys())
            print(
                "Warning: Some edges are connecting vertices that are not"
                + "in this graph. Those vertices are added into the graph.",
                file=sys.stderr,
            )

    def get_vertices(self) -> Set[Vertex]:
        return self.vertices

    def get_edges(self) -> Tuple[WeightedEdge]:
        list_of_edge_list = self.adj_edge_list.values()
        return tuple(e for adj_edges in list_of_edge_list for e in adj_edges)

    def get_neighbors(self, source: Vertex) -> Set[Vertex]:
        edges = self.adj_edge_list.get(source, [])
        return set(e.get_dest() for e in edges)

    def get_edge(self, source: Vertex, dest: Vertex) -> WeightedEdge:
        edges = self.adj_edge_list[source]
        for edge in edges:
            if edge.get_dest() == dest:
                return edge


class Vertex:
    num_vertex = 0

    def __init__(self, name: str = None):
        self.name = name or str(Vertex.num_vertex)
        self.num = Vertex.num_vertex
        Vertex.num_vertex += 1

    def __repr__(self):
        return f"<Vertex; name={self.name}>"

    def __hash__(self):
        return self.num


class WeightedEdge:
    """Weighted Directed Edge"""

    def __init__(
        self, vertex_pair: Tuple[Vertex, Vertex], weight: Union[int, float]
    ):
        self.vertex_pair = vertex_pair
        self.weight = weight

    def __repr__(self):
        return (
            f"<WeightedEdge; {self.vertex_pair[0]} -> {self.vertex_pair[1]}, "
            + f"weight={self.weight}>"
        )

    def get_source(self) -> Vertex:
        return self.vertex_pair[0]

    def get_dest(self) -> Vertex:
        return self.vertex_pair[1]

    def get_weight(self) -> Union[int, float]:
        return self.weight
