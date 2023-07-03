"""
Author: Taanileka Maama
Student ID: 005887076
"""
import os
from datetime import datetime

from models.Driver import Driver
from models.Package import Package
from models.Truck import Truck
from utils.DriverPool import DriverPool
from utils.data import get_locations_from_csv, get_distances_from_csv, get_packages_from_csv
from utils.time import get_today_datetime
from views.ui import ui


def get_project_root():
    """Return the absolute path of the project's root directory."""
    current_path = os.path.abspath(__file__)  # Get the absolute path of the current file
    root_path = os.path.dirname(current_path)  # Get the directory containing the current file

    # Traverse up the directory tree until we find a specific file or reach the root
    while not os.path.isfile(os.path.join(root_path, 'README.md')) and root_path != '/':
        root_path = os.path.dirname(root_path)

    return root_path


PACKAGE_CSV = os.path.join(get_project_root(), 'data/package.csv')
LOCATION_CSV = os.path.join(get_project_root(), 'data/address.csv')
DISTANCE_CSV = os.path.join(get_project_root(), 'data/distance.csv')

if __name__ == "__main__":
    # First let's get all the locations
    locations = get_locations_from_csv(LOCATION_CSV)
    graph = get_distances_from_csv(DISTANCE_CSV, locations)
    # Secondly, we get all the package information
    packages: list[Package] = get_packages_from_csv(PACKAGE_CSV, locations)
    # Next we get our trucks instantiated
    truck_one = Truck(1, locations[0], graph)
    truck_two = Truck(2, locations[0], graph)
    truck_three = Truck(3, locations[0], graph)
    # truck_pool = TruckPool([truck_one, truck_two, truck_three])
    # Then we can instantiate our driver_pool which is where drivers wait to be assigned a truck
    driver_pool = DriverPool([Driver(), Driver()])

    for num in [0, 3, 6, 7, 12, 13, 14, 15, 28, 29, 30, 31, 33, 36, 38, 39]:
        truck_one.load_truck(packages[num])
    for num in [2, 5, 9, 10, 11, 16, 17, 19, 20, 21, 22, 23, 24, 25, 35, 37]:
        truck_two.load_truck(packages[num])
    for num in [1, 4, 8, 18, 26, 27, 32, 34]:
        truck_three.load_truck(packages[num])

    # Now the trucks have been loaded we need to get a driver assigned to the truck and
    truck_one.assign_driver(driver_pool.get_available_driver())
    truck_two.assign_driver(driver_pool.get_available_driver())

    today = datetime.today()
    truck_one.run_route(get_today_datetime(8))
    truck_two.run_route(get_today_datetime(9, 5))
    driver_pool.add_driver_to_pool(truck_one.release_driver())

    truck_three.assign_driver(driver_pool.get_available_driver())
    truck_three.run_route(truck_one.current_time)
    trucks = [truck_one, truck_two, truck_three]

    ui(trucks, packages)

