from utils.HashTable import HashTable


class Graph:
    """
    A graph data structure. This implementation uses an adjacency list.
    This graph is from the WGU example cited below:
    Citation: C950 Zybooks Chapter 6.12 Example
    """
    def __init__(self):
        self.adjacency_list: HashTable = HashTable()
        self.edge_weights: HashTable = HashTable()

    def add_vertex(self, new_vertex):
        if self.adjacency_list.get_val(new_vertex) is None:
            self.adjacency_list.set_val(new_vertex, [])

    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights.set_val((from_vertex, to_vertex), weight)
        self.adjacency_list.get_val(from_vertex).append(to_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    def get_edge_weight(self, from_vertex, to_vertex):
        distance = self.edge_weights.get_val((from_vertex, to_vertex))
        return distance
