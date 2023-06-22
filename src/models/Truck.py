from typing import Any
from calendar import timegm
from datetime import datetime as dt, timedelta as td
from models import Package, Driver, Location
from utils import Graph, get_downtown_map, get_locations, ChainingHashTable


class Truck(object):
    """Class definition for the Truck object."""

    def __init__(self, truck_id: int) -> None:
        self.truck_id: int = truck_id
        self.today = dt.today()
        self.packages: list[Package] = []
        self.package_manager: ChainingHashTable = ChainingHashTable(11)
        self.addresses_to_deliver_to: list[Location] = []
        self.locations: list[Location] = get_locations('data/address.csv')
        self.next_location = None
        self.driver: Driver or None = None
        self.current_time: dt or None = None
        self.downtown_map: Graph = get_downtown_map('data/distance.csv', self.locations)
        # TODO: Define a starting location which should be the hub.
        self.current_location: Location = self.locations[0]
        self.accumulated_miles = 0

    def __getitem__(self, item) -> Any:
        return self[item]

    def __setitem__(self, key, value) -> None:
        self[key] = value

    def is_full(self):
        return len(self.packages) >= 16

    def load_truck(self, package: Package) -> bool:
        """
        Loads the truck with the package parameter unless the truck is full
        Runs O(n) due to the check if the package.address is in self.locations_to_deliver_to
        :param package:
        :return:
        """
        if self.is_full():
            return False
        self.packages.append(package)
        package.truck_id = self.truck_id
        loc: Location or None = Location.find_by_address(self.locations, package.address)
        if loc is not None and loc not in self.addresses_to_deliver_to:
            self.addresses_to_deliver_to.append(loc)
        return True

    def assign_driver(self, driver: Driver) -> None:
        self.driver = driver

    def travel_time(self, distance: float) -> None:
        """
        Simple conversion of the distance from truck's current location
        to the next POI for delivery. O(1)
        """
        hours_traveling = distance / 18
        self.current_time += td(hours=hours_traveling)

    def travel(self, to: Location):
        distance: float = self.downtown_map.route_distances[(self.current_location, to)]
        self.accumulated_miles += distance
        self.travel_time(distance)

    def priority_sort_packages(self) -> None:
        """
        Sorts the packages by priority (deadline).
        Time Complexity: O(n)
        :return:
        """
        def sort_by_priority(package):
            deadline = timegm(package.deadline.timetuple())
            location = Location.find_by_address(self.locations, package.address)
            return deadline + location.distance

        self.packages.sort(key=sort_by_priority)

    def deliver_packages(self, departure_time):
        self.priority_sort_packages()
        # This method start with labeling all packages as in transit. This is O(1) most likely
        # due to us knowing the max will always be 16.
        self.current_time: dt = departure_time
        for p in self.packages:
            p.status = 'In transit'
        while len(self.addresses_to_deliver_to) > 0:
            # First we calculate all the current distances
            self.get_distances_from_current_loc()
            self.dijkstra_shortest_path()
            for p in self.packages:
                if p.status != 'DELIVERED':
                    p = p
                    break
            next_loc = Location.find_by_address(self.locations, p.address)
            self.addresses_to_deliver_to.remove(next_loc)
            path = self.get_shortest_path(next_loc)
            self.traverse_path(path)
            loc_packages: list[Package] = list(
                filter(lambda p: p.address == next_loc.address, self.packages))
            for p in loc_packages:
                self.deliver_package(p)

    def deliver_package(self, package):
        package.update('DELIVERED', self.current_time)
        self.package_manager.remove(package)

    # def find_nearest_loc(self):
    #     """
    #     An implementation of Dijkstra's shortest path with terminology
    #     that is used for WGUPS app. Runs
    #     TODO: Add citation to WGU
    #     :return:
    #     """
    #     # starting_location has a distance of 0 from itself
    #     self.current_location.distance = 0
    #
    #     # One location is removed with each iteration; repeat until the list is empty
    #     closest_i = 0
    #     closest_loc: Location = Location.find_by_address(self.locations, self.addresses_to_deliver_to[0])
    #     # Visit location with min distance from starting_location
    #     for i in range(1, len(self.addresses_to_deliver_to)):
    #         closest_distance = self.downtown_map.route_distances[
    #             (self.current_location.address, closest_loc.address)]
    #         searched_loc = Location.find_by_address(self.locations, self.addresses_to_deliver_to[i])
    #         searched_loc_distance = self.downtown_map.route_distances[
    #             (self.current_location.address, searched_loc.address)]
    #         packages_closest = Package.find_by_address(self.packages, closest_loc.address)
    #         closest_has_deadline = Package.packages_have_deadline(packages_closest)
    #         packages_searched_loc = Package.find_by_address(self.packages, searched_loc.address)
    #         searched_loc_has_deadline = Package.packages_have_deadline(packages_searched_loc)
    #         if searched_loc_distance < closest_distance or (searched_loc_has_deadline and not closest_has_deadline):
    #             closest_loc = searched_loc
    #             closest_i = i
    #     self.addresses_to_deliver_to.pop(closest_i)
    #     return closest_loc

    def get_distances_from_current_loc(self) -> None:
        """
        Sets the distance attribute of each location in the adjacency list.
        Time Complexity: O(n)
        :return: None
        """
        for loc in self.downtown_map.adjacency_list[self.current_location]:
            loc.distance = self.downtown_map.route_distances[(self.current_location, loc)]

    def dijkstra_shortest_path(self) -> None:
        """

        :return:
        """
        self.get_distances_from_current_loc()
        # Put all vertices in an unvisited queue.
        unvisited_queue: list[Location] = []
        for loc in self.downtown_map.adjacency_list:
            unvisited_queue.append(loc)
        # Start_vertex has a distance of 0 from itself
        self.current_location.distance = 0.0

        # One vertex is removed with each iteration; repeat until the list is
        # empty.
        while len(unvisited_queue) > 0:
            # Visit vertex with minimum distance from start_vertex
            smallest_index = 0
            for i in range(1, len(unvisited_queue)):
                if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                    smallest_index = i
            current_loc = unvisited_queue.pop(smallest_index)

            # Check potential path lengths from the current vertex to all neighbors.
            adj_location: Location
            for adj_location in self.downtown_map.adjacency_list[current_loc]:
                distance: float = self.downtown_map.route_distances[(current_loc, adj_location)]
                alternative_path_distance: float = current_loc.distance + distance

                # If shorter path from start_vertex to adj_location is found,
                # update adj_location's distance and predecessor
                if alternative_path_distance < adj_location.distance:
                    adj_location.distance = alternative_path_distance
                    adj_location.pred_loc = current_loc

    def get_shortest_path(self, end_location: Location) -> list[Location]:
        # Start from end_location and build the path backwards.
        path: list[Location] = []
        current_loc: Location = end_location
        while current_loc is not self.current_location and current_loc is not None:
            path.insert(0, current_loc)
            current_loc = current_loc.pred_loc

        # Return the path the object should move.
        return path

    def traverse_path(self, path: list[Location]):
        for loc in path:
            self.travel(loc)

    def release_driver(self) -> Driver:
        driver: Driver = self.driver
        self.driver = None
        return driver
