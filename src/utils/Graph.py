from models.Location import Location
from utils.ChainingHashTable import ChainingHashTable


class Graph:
    def __init__(self):
        """
        Map is a graph that links POIs (vertices) to routes (edges).
        """
        self.adjacency_list = {}
        self.route_distances = {}

    def add_location(self, new_loc):
        self.adjacency_list[new_loc.address] = []

    def add_directed_route(self, from_loc: Location, to_loc: Location, distance: float):
        """

        :param from_loc:
        :param to_loc:
        :param distance:
        """
        self.route_distances[(from_loc.address, to_loc.address)] = distance
        self.adjacency_list[from_loc.address].append(to_loc.address)

    def add_route(self, loc_a: Location, loc_b: Location, distance: float):
        self.add_directed_route(loc_a, loc_b, distance)
        self.add_directed_route(loc_b, loc_a, distance)
