"""
Author: Taanileka Maama
Student ID: 005887076
"""
from models.Location import Location
from models.Package import Package
from models.Truck import Truck
from utils.ChainingHashTable import ChainingHashTable
from utils.DriverPool import DriverPool
from utils.get_csv import get_packages, get_downtown_map, get_locations
from utils.dikstras_shortest_path import dijkstra_shortest_path
from utils.trucks import load_truck_one, load_truck_two, load_truck_three

if __name__ == "__main__":
    # First let's get all the locations
    locations: list[Location] = get_locations('../data/address.csv')
    # Secondly, we get all the packages that grouped based of a hash of their location
    packages: ChainingHashTable = get_packages('../data/package.csv')
    downtown_map = get_downtown_map('../data/distance.csv', '../data/address.csv')
    dijkstra_shortest_path(downtown_map, locations[0])
    # Next we get our trucks ready to load
    truck_one = Truck(downtown_map, locations[0], locations)
    truck_two = Truck(downtown_map, locations[0], locations)
    truck_three = Truck(downtown_map, locations[0], locations)
    # Then we can instantiate our driver_pool which is where drivers wait to be assigned a truck
    driver_pool = DriverPool()
    # Our first pass through the HashTable will not load the trucks with all the packages.
    leftover_packages = []
    # Iterate through locations and see where we need to deliver to.
    for loc in locations:
        bucket_list: list[Package] = packages.get_bucket_list(loc.address)
        # Get specified packages into the correct trucks
        while len(bucket_list) > 0:
            package = bucket_list.pop()
            loaded_successfully = False
            if package.notes == 'Can only be on truck 2' or package.address in truck_two.addresses_to_deliver_to or package.notes is not None and 'Must be delivered' in package.notes:
                loaded_successfully = truck_two.load_truck(package)
            elif package.notes is not None and 'Delayed on flight' in package.notes or package.address in truck_three.addresses_to_deliver_to:
                loaded_successfully = truck_three.load_truck(package)
            elif package.deadline == '10:30:00' or package.address in truck_one.addresses_to_deliver_to:
                loaded_successfully = truck_one.load_truck(package)
            if not loaded_successfully:
                leftover_packages.append(package)

    # Then we'll iterate over the leftovers packages and load the trucks to max capacity or
    # until we run out of leftover packages.
    while len(leftover_packages) > 0 or len(truck_one.packages) == 16 and len(truck_two.packages) == 16 and len(
            truck_three.packages) == 16:
        package = leftover_packages.pop()
        if len(truck_one.packages) < 16:
            truck_one.load_truck(package)
        elif len(truck_two.packages) < 16:
            truck_two.load_truck(package)
        elif len(truck_three.packages) < 16:
            truck_three.load_truck(package)

    # Now the trucks have been loaded we need to get a driver assigned to the truck and
    truck_one.assign_driver(driver_pool.enqueue_driver())
    truck_two.assign_driver(driver_pool.enqueue_driver())

    truck_one.deliver_packages()
    truck_two.deliver_packages()
    driver_pool.add_driver_to_pool(truck_one.unassign_driver())

    truck_three.assign_driver(driver_pool.enqueue_driver())
    truck_three.deliver_packages(truck_one.current_time)

    # After deliveries get all accumulated miles from the trucks
    print(
        f"Total distance traveled: {truck_one.accumulated_miles + truck_two.accumulated_miles + truck_three.accumulated_miles}")
    print(f"Truck one Times: {truck_one.current_time}")
    print(f"Truck Two Times: {truck_two.current_time}")
    print(f"Truck three Times: {truck_three.current_time}")
