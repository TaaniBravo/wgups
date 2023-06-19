from typing import Any
from models import Package, Driver
from datetime import datetime as dt, timedelta as td

from models.Location import Location
from utils.Graph import Graph


class Truck(object):
    """Class definition for the Truck object."""

    def __init__(self, downtown_map: Graph, current_location: Location, locations: list[Location]) -> None:
        self.loaded = False
        self.ready = False
        self.packages = []
        self.addresses_to_deliver_to = []
        self.locations = locations
        self.next_location = None
        self.driver = None
        self.current_time: dt or None = None
        self.downtown_map = downtown_map
        # TODO: Define a starting location which should be the hub.
        self.current_location = current_location
        self.accumulated_miles = 0

    def __getitem__(self, item) -> Any:
        return self[item]

    def __setitem__(self, key, value) -> None:
        self[key] = value

    def load_truck(self, package: Package) -> bool:
        """
        Loads the truck with the package parameter unless the truck is full
        Runs O(n) due to the check if the package.address is in self.locations_to_deliver_to
        :param package:
        :return:
        """
        if len(self.packages) >= 16:
            return False
        self.packages.append(package)
        if package.address not in self.addresses_to_deliver_to:
            self.addresses_to_deliver_to.append(package.address)
        return True

    def start_route(self, address) -> None:
        # self.find_nearest_loc(self.current_location)
        pass

    def assign_driver(self, driver: Driver) -> None:
        self.driver = driver
        if self.loaded:
            self.ready = True

    def leave_port(self, departure_time: dt) -> None:
        self.current_time = departure_time

    def travel_time(self, distance: float) -> None:
        """
        Simple conversion of the distance from truck's current location
        to the next POI for delivery. O(1)
        """
        seconds_in_transit = distance * 3600 / 18
        self.current_time += td(seconds=seconds_in_transit)

    def travel(self, to: Location):
        distance: float = self.downtown_map.route_distances[(self.current_location.address, to.address)]
        self.accumulated_miles += distance
        self.travel_time(distance)

    def deliver_packages(self, departure_time=dt(2023, 6, 25, 8)):
        # This method start with labeling all packages as in transit. This is O(1) most likely
        # due to us knowing the max will always be 16.
        self.current_time: dt = departure_time
        for p in self.packages:
            p.status = 'In transit'
        while len(self.addresses_to_deliver_to) > 0:
            # Find the nearest location that the truck can deliver to.
            next_loc = self.find_nearest_loc()
            # Next get the distance between the next location and the truck's current location
            self.travel(next_loc)
            loc_packages: list[Package] = list(
                filter(lambda package: package.address == next_loc.address, self.packages))
            for p in loc_packages:
                self.deliver_package(p)

    def deliver_package(self, package):
        package.status = 'Delivered'
        package.delivery_time = self.current_time

    def find_nearest_loc(self):
        """
        An implementation of Dijkstra's shortest path with terminology
        that is used for WGUPS app. Runs
        TODO: Add citation to WGU
        :return:
        """
        # starting_location has a distance of 0 from itself
        self.current_location.distance = 0

        # One location is removed with each iteration; repeat until the list is empty
        closest_i = 0
        closest_loc: Location = Location.find_by_address(self.locations, self.addresses_to_deliver_to[0])
        # Visit location with min distance from starting_location
        for i in range(1, len(self.addresses_to_deliver_to)):
            closest_distance = self.downtown_map.route_distances[
                (self.current_location.address, closest_loc.address)]
            unvisited_loc = Location.find_by_address(self.locations, self.addresses_to_deliver_to[i])
            distance = self.downtown_map.route_distances[
                (self.current_location.address, unvisited_loc.address)]
            if distance < closest_distance:
                closest_loc = unvisited_loc
                closest_i = i

        self.addresses_to_deliver_to.pop(closest_i)
        return closest_loc

    def unassign_driver(self):
        driver = self.driver
        self.driver = None
        return driver
