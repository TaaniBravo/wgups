from typing import Any
from calendar import timegm
from datetime import datetime as dt, timedelta as td
from models import Package, Driver, Location
from utils import Graph, get_downtown_map, get_locations, ChainingHashTable
from config import DELIVERED


class Truck(object):
    """Class definition for the Truck object."""

    def __init__(self, truck_id: int) -> None:
        self.truck_id: int = truck_id
        self.packages: list[Package] = []
        self.addresses_to_deliver_to: list[Location] = []
        self.locations: list[Location] = get_locations('data/address.csv')
        self.driver: Driver or None = None
        self.current_time: dt or None = None
        self.downtown_map: Graph = get_downtown_map('data/distance.csv', self.locations)
        # TODO: Define a starting location which should be the hub.
        self.current_location: Location = self.locations[0]
        self.accumulated_miles: float = 0.0

    def __getitem__(self, item) -> Any:
        """
        Returns an instances of Truck's properties
        Time Complexity: O(1)
        Space Complexity: O(1)
        :param item:
        :return:
        """
        return self[item]

    def __setitem__(self, key, value) -> None:
        """
        Set a value for an instance of Truck's properties
        Time Complexity: O(1)
        Space Complexity: O(1)
        :param key:
        :param value:
        :return:
        """
        self[key] = value

    def is_full(self):
        return len(self.packages) >= 16

    def load_truck(self, package: Package) -> bool:
        """
        Loads the truck with the package parameter unless the truck is full.
        Returns True if the package was loaded, False otherwise.
        Time complexity: O(n)
        Space complexity: O(1)
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
        """
        Assigns a driver to the truck.
        Time Complexity: O(1)
        Space Complexity: O(1)
        :param driver:
        :return:
        """
        self.driver = driver

    def travel_time(self, distance: float) -> None:
        """
        Simple conversion of the distance from truck's current location
        to the next POI for delivery. O(1)
        """
        hours_traveling: float = distance / 18
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
            return deadline

        self.packages.sort(key=sort_by_priority)

    def deliver_packages(self, departure_time):
        self.priority_sort_packages()
        # This method start with labeling all packages as in transit. This is O(1) most likely
        # due to us knowing the max will always be 16.
        self.current_time: dt = departure_time
        for p in self.packages:
            p.set_in_transit()
        while len(self.addresses_to_deliver_to) > 0:
            # First we find the nearest location to the truck's current location.
            next_loc = self.get_nearest_location()
            # Then we travel to that location.
            self.travel(next_loc)
            # Then we deliver all packages for that location.
            loc_packages: list[Package] = list(
                filter(lambda pa: pa.address == next_loc.address, self.packages))
            for p in loc_packages:
                self.deliver_package(p)
        # After all packages have been delivered, we return to the hub.
        self.travel(self.locations[0])

    def deliver_package(self, package):
        """
        Sets the package as delivered.
        :param package:
        :return:
        """
        package.set_as_delivered(self.current_time)

    def get_distances_from_current_loc(self) -> None:
        """
        Sets the distance attribute of each location in the adjacency list to the current location.
        Time Complexity: O(n)
        Space Complexity: O(1)
        :return: None
        """
        for loc in self.addresses_to_deliver_to:
            loc.distance = self.downtown_map.route_distances[(self.current_location, loc)]

    def release_driver(self) -> Driver:
        """
        Releases the driver assigned from the truck.
        Time Complexity: O(1)
        Space Complexity: O(1)
        :return:
        """
        driver: Driver = self.driver
        self.driver = None
        return driver

    # Nearest neighbor algorithm
    def get_nearest_location(self) -> Location:
        """
        An implementation of the nearest neighbor algorithm. This algorithm
        finds the nearest location to the current location.
        Time Complexity: O(2n) -> O(n) where n is the number of addresses to deliver to.
        Space Complexity: O(n)
        :return: A list of locations in the order they should be visited.
        """
        self.get_distances_from_current_loc()
        priority_packages = self.get_priority_packages()
        locations = list(map(lambda p: Location.find_by_address(self.locations, p.address), priority_packages))
        if len(locations) == 1:
            return locations[0]
        nearest_loc_i = 0
        for i, current_loc in enumerate(self.addresses_to_deliver_to):
            nearest_loc = self.addresses_to_deliver_to[nearest_loc_i]

            if current_loc.distance < nearest_loc.distance:
                nearest_loc_i = i

        return self.addresses_to_deliver_to.pop(nearest_loc_i)

    def find_first_undelivered_package(self) -> Package:
        """
        Finds the first undelivered package in the truck.
        Time Complexity: O(n)
        :return: The first undelivered package.
        """
        for p in self.packages:
            if p.status != DELIVERED:
                return p

    def get_priority_packages(self):
        priority_package = self.find_first_undelivered_package()
        return list(
            filter(lambda p: p.deadline == priority_package.deadline, self.packages))
