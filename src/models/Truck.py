from datetime import datetime, timedelta

from utils import Graph
from models.Driver import Driver
from models.Location import Location
from models.Package import Package

TRUCK_MAX_PACKAGES = 16
TRUCK_MAX_SPEED = 18  # MPH


class Truck:
    def __init__(self, id: int, location: Location, graph: Graph):
        self.id: int = id
        self.packages: list[Package] = []
        self.delivery_locations: list[Location] = []
        self.delayed_packages: list[Package] = []
        self.current_time: datetime or None = None
        self.departure_time: datetime or None = None
        self.current_location: Location = location
        self.accumulated_distance: float = 0.0
        self.hub: Location = location
        self.driver: Driver or None = None
        self.graph: Graph = graph

    def __setitem__(self, key, value):
        self[key] = value

    def __getitem__(self, item):
        return self[item]

    def is_full(self) -> bool:
        return len(self.packages) == TRUCK_MAX_PACKAGES

    def load_truck(self, package: Package) -> bool:
        if self.is_full():
            return False
        if package.delayed:
            self.delayed_packages.append(package)
        else:
            self.packages.append(package)
            if package.location not in self.delivery_locations:
                self.delivery_locations.append(package.location)
        package.truck_id = self.id
        return True

    def assign_driver(self, driver: Driver) -> None:
        self.driver = driver

    def release_driver(self) -> Driver:
        driver = self.driver
        driver.set_availability()
        self.driver = None
        return driver

    def run_route(self, departure_time: datetime or None = None, recursive: bool = False) -> None:
        # First let's start by setting the departure time and truck's current time
        if not recursive:
            self.departure_time = departure_time
            self.current_time = departure_time
        self.set_packages_en_route()
        # Now set packages to en route
        self.update_distances_from_current_location()
        # Now let's start the route
        while len(self.delivery_locations) > 0:
            # First let's find the nearest location
            next_loc = self.find_nearest_location()
            # Now let's travel to that location
            self.travel_to_location(next_loc)
            # Now let's deliver packages at that location
            self.deliver_packages()
            # Then check for any updates to delayed packages
            self.update_delayed_packages()
        # Before we return, make sure there's no delayed packages
        if len(self.delayed_packages):
            self.wait_for_delayed_packages()
            self.run_route()
        self.travel_to_location(self.hub)

    def wait_for_delayed_packages(self) -> None:
        shortest_delayed_time = self.delayed_packages[0].delayed_datetime
        for package in self.delayed_packages:
            if package.delayed_datetime < shortest_delayed_time:
                shortest_delayed_time = package.delayed_datetime

        self.current_time = shortest_delayed_time

    def find_nearest_location(self) -> Location:
        if len(self.delivery_locations) == 1:
            return self.delivery_locations.pop()
        nearest_location: Location = self.delivery_locations[0]
        for location in self.delivery_locations:
            if location.distance < nearest_location.distance:
                nearest_location = location

        self.delivery_locations.remove(nearest_location)
        return nearest_location

    def travel_to_location(self, location: Location) -> None:
        self.accumulated_distance += location.distance
        self.current_location = location
        hours_traveling = location.distance / TRUCK_MAX_SPEED
        self.current_time += timedelta(hours=hours_traveling)
        # Next let's update the distances from the current location
        self.update_distances_from_current_location()

    def update_delayed_packages(self) -> None:
        for package in self.delayed_packages:
            if self.current_time > package.delayed_datetime:
                package.delayed = False
                self.delayed_packages.remove(package)
                self.load_truck(package)
                if package.id == 9:
                    package.address = '410 S State St'
                    package.city = 'Salt Lake City'
                    package.state = 'UT'
                    package.zip_code = '84111'

    def deliver_packages(self) -> None:
        for package in self.packages:
            if package.location.id == self.current_location.id:
                package.status = 'Delivered'
                package.delivery_time = self.current_time

    def update_distances_from_current_location(self):
        for location in self.delivery_locations:
            location.distance = self.graph.get_edge_weight(self.current_location, location)
        self.hub.distance = self.graph.get_edge_weight(self.current_location, self.hub)

    def set_packages_en_route(self) -> None:
        for p in self.packages:
            p.status = 'En Route'
            p.en_route_time = self.current_time
        for p in self.delayed_packages:
            p.status = 'En Route'
            p.en_route_time = self.current_time
