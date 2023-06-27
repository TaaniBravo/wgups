"""
Author: Taanileka Maama
Student ID: 005887076
"""
from datetime import datetime
from lib import Package, Truck, Location, DriverPool, UI, Driver
from lib.TruckPool import TruckPool

if __name__ == "__main__":
    # First let's get all the locations
    locations = Location.get_locations_from_csv('data/address.csv')
    # Secondly, we get all the package information
    packages: list[Package] = Package.get_packages_from_csv('data/package.csv', locations)
    # Next we get our trucks instantiated
    truck_one = Truck(1, locations)
    truck_two = Truck(2, locations)
    truck_three = Truck(3, locations)
    truck_pool = TruckPool([truck_one, truck_two, truck_three])
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
    truck_one.deliver_packages(datetime(today.year, today.month, today.day, 8))
    truck_two.deliver_packages(datetime(today.year, today.month, today.day, 9, 5))
    driver_pool.add_driver_to_pool(truck_one.release_driver())

    truck_three.assign_driver(driver_pool.get_available_driver())
    truck_three.deliver_packages(truck_one.current_time)

    ui = UI(truck_pool, packages)
    ui.start()
