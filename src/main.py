"""
Author: Taanileka Maama
Student ID: 005887076
"""
from ui import ui
from datetime import datetime
from models import Package, Truck
from utils import DriverPool, get_packages

if __name__ == "__main__":
    # First let's get all the locations
    # Secondly, we get all the packages that grouped based of a hash of their location
    packages: list[Package] = get_packages('data/package.csv')
    # Next we get our trucks instantiated
    truck_one = Truck(1)
    truck_two = Truck(2)
    truck_three = Truck(3)
    # Then we can instantiate our driver_pool which is where drivers wait to be assigned a truck
    driver_pool = DriverPool()
    # Our first pass through the HashTable will not load the trucks with all the packages.
    leftover_packages = []
    # Iterate through locations and see where we need to deliver to.
    for num in [0, 3, 5, 6, 16, 18, 20, 24, 28, 30, 39]:
        truck_one.load_truck(packages[num])
    for num in [2, 4, 9, 12, 13, 14, 15, 17, 19, 20, 29, 33, 35, 36, 37, 38]:
        truck_two.load_truck(packages[num])
    for num in [1, 7, 8, 10, 11, 21, 22, 23, 25, 26, 27, 31, 32, 34]:
        truck_three.load_truck(packages[num])

    # Try 2
    # for package in packages:
    #     if isinstance(package.deadline, datetime) and package.notes is None or package.notes is not None and 'Must be delivered' in package.notes or package.address in truck_one.addresses_to_deliver_to:
    #         truck_one.load_truck(package)
    #     elif isinstance(package.deadline, datetime) or (package.notes is not None) or package.address in truck_two.addresses_to_deliver_to:
    #         truck_two.load_truck(package)
    #     if package.deadline == "EOD" or package.address in truck_three.addresses_to_deliver_to:
    #         truck_three.load_truck(package)

    # Now the trucks have been loaded we need to get a driver assigned to the truck and
    truck_one.assign_driver(driver_pool.enqueue_driver())
    truck_two.assign_driver(driver_pool.enqueue_driver())

    today = datetime.today()
    truck_two.deliver_packages(datetime(today.year, today.month, today.day, 8))
    truck_one_departure_time = datetime(today.year, today.month, today.day, 9, 5)
    truck_one.deliver_packages(truck_one_departure_time)
    driver_pool.add_driver_to_pool(truck_one.release_driver())

    truck_three.assign_driver(driver_pool.enqueue_driver())
    truck_three.deliver_packages(truck_one.current_time)

    # After deliveries get all accumulated miles from the trucks
    print(
        f"Total distance traveled: {truck_one.accumulated_miles + truck_two.accumulated_miles + truck_three.accumulated_miles}")
    print(f"Truck one Times: {truck_one.current_time} Miles: {truck_one.accumulated_miles}")
    print(f"Truck Two Times: {truck_two.current_time} Miles: {truck_two.accumulated_miles}")
    print(f"Truck three Times: {truck_three.current_time} Miles: {truck_three.accumulated_miles}")

    total_packages_delivered = 0
    for p in packages:
        if p.delivery_time is not None:
            total_packages_delivered += 1
        print(p.__str__())

    print(f"Total packages delivered: {total_packages_delivered}")

    ui()
