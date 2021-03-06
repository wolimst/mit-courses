import pytest
from graph import (
    Graph,
    Vertex,
    WeightedEdge,
    breadth_first_search,
    depth_first_search,
    dijkstra,
    bellman_ford,
)


class TestDirectedGraph:
    # TODO: Do tests with more comprehensive test cases.

    def test_build_graph(self):
        num_vertex = 10
        v = [Vertex() for i in range(num_vertex)]
        e = [WeightedEdge((v[i], v[i + 1]), i) for i in range(num_vertex - 1)]
        g = Graph(v, e)
        assert set(v) == g.get_vertices()
        assert len(e) == len(g.get_edges())

    def test_breadth_first_search(self):
        """ A ← B → C
            ↓ ↘ ↑ ↗ ↓
            D → E   F
        """
        num_vertex = 6
        v = [Vertex() for i in range(num_vertex)]
        e = [
            WeightedEdge((v[0], v[3]), 1),
            WeightedEdge((v[0], v[4]), 1),
            WeightedEdge((v[1], v[0]), 1),
            WeightedEdge((v[1], v[2]), 1),
            WeightedEdge((v[2], v[5]), 1),
            WeightedEdge((v[3], v[4]), 1),
            WeightedEdge((v[4], v[1]), 1),
            WeightedEdge((v[4], v[2]), 1),
        ]
        g = Graph(v, e)
        parent_dict = breadth_first_search(g, v[0])
        assert parent_dict[v[0]] is None
        assert parent_dict[v[1]] is v[4]
        assert parent_dict[v[2]] is v[4]
        assert parent_dict[v[3]] is v[0]
        assert parent_dict[v[4]] is v[0]
        assert parent_dict[v[5]] is v[2]

    def test_depth_first_search(self):
        """ A ← B   C
            ↓ ↘ ↑ ↗ ↓
            D → E   F
        """
        num_vertex = 6
        v = [Vertex() for i in range(num_vertex)]
        e = [
            WeightedEdge((v[0], v[3]), 1),
            WeightedEdge((v[0], v[4]), 1),
            WeightedEdge((v[1], v[0]), 1),
            WeightedEdge((v[2], v[5]), 1),
            WeightedEdge((v[3], v[4]), 1),
            WeightedEdge((v[4], v[1]), 1),
            WeightedEdge((v[4], v[2]), 1),
        ]
        g = Graph(v, e)
        finished = depth_first_search(g, v[0])
        assert finished == [v[1], v[5], v[2], v[4], v[3], v[0]]

    def test_dijkstra(self):
        """C → → → → → D → +
           ↓ ↖       ↗ ↓   ↓
           ↓   A → B   ↙   ↓
           ↓       ↓ ↙     ↓
           + → → → E → → → F
        """
        v = [Vertex(name) for name in "ABCDEF"]
        e = [
            WeightedEdge((v[0], v[1]), 10),  # A -> B
            WeightedEdge((v[0], v[2]), 20),  # A -> C
            WeightedEdge((v[1], v[3]), 50),  # B -> D
            WeightedEdge((v[1], v[4]), 10),  # B -> E
            WeightedEdge((v[2], v[3]), 20),  # C -> D
            WeightedEdge((v[2], v[4]), 33),  # C -> E
            WeightedEdge((v[3], v[4]), 20),  # D -> E
            WeightedEdge((v[3], v[5]), 2),  # D -> F
            WeightedEdge((v[4], v[5]), 1),  # E -> F
        ]
        g = Graph(v, e)
        distance, parent = dijkstra(g, v[0])

        dist_ans = {v[0]: 0, v[1]: 10, v[2]: 20, v[3]: 40, v[4]: 20, v[5]: 21}
        parent_ans = {
            v[0]: None,
            v[1]: v[0],
            v[2]: v[0],
            v[3]: v[2],
            v[4]: v[1],
            v[5]: v[4],
        }
        assert dist_ans == distance
        assert parent_ans == parent

    def test_bellman_ford(self):
        """ A ← B → C
            ↓ ↘ ↑ ↗ ↓
            D → E   F
        """
        v = [Vertex(name) for name in "ABCDEF"]
        e = [
            WeightedEdge((v[0], v[3]), -1),
            WeightedEdge((v[0], v[4]), 10),
            WeightedEdge((v[1], v[0]), -3),
            WeightedEdge((v[1], v[2]), 5),
            WeightedEdge((v[2], v[5]), -1),
            WeightedEdge((v[3], v[4]), 7),
            WeightedEdge((v[4], v[1]), -2),
            WeightedEdge((v[4], v[2]), 4),
        ]
        g = Graph(v, e)
        distance, parent = bellman_ford(g, v[0])
        dist_ans = {v[0]: 0, v[1]: 4, v[2]: 9, v[3]: -1, v[4]: 6, v[5]: 8}
        parent_ans = {
            v[0]: None,
            v[1]: v[4],
            v[2]: v[1],
            v[3]: v[0],
            v[4]: v[3],
            v[5]: v[2],
        }
        assert dist_ans == distance
        assert parent_ans == parent

    def test_bellman_ford_negative_cycle(self):
        """ A ← B → C
            ↓ ↘ ↑ ↗ ↓
            D → E   F
        """
        num_vertex = 6
        v = [Vertex() for i in range(num_vertex)]
        e = [  # negative cycle in A -> D -> E -> B -> A
            WeightedEdge((v[0], v[3]), -1),  # A -> D
            WeightedEdge((v[0], v[4]), 10),  # A -> E
            WeightedEdge((v[1], v[0]), -3),  # B -> A
            WeightedEdge((v[1], v[2]), 5),  # B -> C
            WeightedEdge((v[2], v[5]), -1),  # C -> F
            WeightedEdge((v[3], v[4]), 5),  # D -> E
            WeightedEdge((v[4], v[1]), -2),  # E -> B
            WeightedEdge((v[4], v[2]), 4),  # E -> C
        ]
        g = Graph(v, e)
        with pytest.raises(RuntimeError):
            distance, parent = bellman_ford(g, v[0])
