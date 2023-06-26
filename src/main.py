"""
Author: Taanileka Maama
Student ID: 005887076
"""
from datetime import datetime
from lib import Package, Truck, Location, DriverPool, UI
from lib.TruckPool import TruckPool


def determine_best_truck(package: Package, trucks: list[Truck]) -> Truck:
    if len(trucks) < 1:
        raise Exception('No trucks available.')
    if len(trucks) == 1:
        return trucks[0]
    for t in trucks:
        t.get_distances_from_current_loc()


if __name__ == "__main__":
    # First let's get all the locations
    # Secondly, we get all the packages that grouped based of a hash of their location
    locations = Location.get_locations_from_csv('data/address.csv')
    packages: list[Package] = Package.get_packages_from_csv('data/package.csv', locations)
    packages_to_load = packages.copy()
    # Next we get our trucks instantiated
    truck_one = Truck(1, locations)
    truck_two = Truck(2, locations)
    truck_three = Truck(3, locations)
    # Then we can instantiate our driver_pool which is where drivers wait to be assigned a truck
    driver_pool = DriverPool()
    # Our first pass through the HashTable will not load the trucks with all the packages.
    leftover_packages = []
    # Iterate through locations and see where we need to deliver to.
    today = datetime.today()
    eod_dt = datetime(today.year, today.month, today.day, 23, 59, 59)
    # for p in packages:
    #     loaded_successfully = False
    #     if p.notes == 'Can only be on truck 2' or p.delivery_location. in truck_two.addresses_to_deliver_to:
    #         loaded_successfully = truck_two.load_truck(p)
    #     elif p.notes is None and p.deadline < eod_dt or p.delivery_location in truck_one.addresses_to_deliver_to:
    #         loaded_successfully = truck_one.load_truck(p)
    #     elif p.deadline == eod_dt or p.delivery_location in truck_three.addresses_to_deliver_to:
    #         loaded_successfully = truck_three.load_truck(p)
    #     if not loaded_successfully:
    #         leftover_packages.append(p)

    truck_one_package_indexes = [14, 0, 12, 13, 15, 19, 28, 30, 39]
    truck_two_package_indexes = [29, 17, 2, 35, 37]
    truck_three_package_indexes = [5, 24]
    for i in truck_one_package_indexes:
        package = packages[i]
        truck_one.load_truck(package)
        packages_to_load.remove(package)
    for i in truck_two_package_indexes:
        package = packages[i]
        truck_two.load_truck(package)
        packages_to_load.remove(package)
    for i in truck_three_package_indexes:
        package = packages[i]
        truck_three.load_truck(package)
        packages_to_load.remove(package)
    # for p in packages_to_load:
    #     package

    # for num in [0, 3, 5, 6, 12, 16, 18, 20, 24, 28, 30, 39]:
    #     truck_one.load_truck(packages[num])
    # for num in [2, 4, 9, 13, 14, 15, 17, 19, 20, 29, 33, 35, 36, 37, 38]:
    #     truck_two.load_truck(packages[num])
    # for num in [1, 7, 8, 10, 11, 21, 22, 23, 25, 26, 27, 31, 32, 34]:
    #     truck_three.load_truck(packages[num])

    # Now the trucks have been loaded we need to get a driver assigned to the truck and
    truck_one.assign_driver(driver_pool.enqueue_driver())
    truck_two.assign_driver(driver_pool.enqueue_driver())

    today = datetime.today()
    truck_two.deliver_packages(datetime(today.year, today.month, today.day, 8))
    truck_one.deliver_packages(datetime(today.year, today.month, today.day, 9, 5, 0))
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

    ui = UI(TruckPool([truck_one, truck_two, truck_three]), packages_to_load)
    ui.start()
