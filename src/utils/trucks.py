from models.Package import Package
from models.Truck import Truck
from utils.ChainingHashTable import ChainingHashTable


def load_truck_one(packages: list[Package], truck: Truck) -> Truck:
    pass


def get_truck_two_list_specifications(package: Package):
    if package.notes == 'Can only be on truck 2':
        return True


def load_truck_two(packages: list[Package], truck: Truck) -> Truck:
    truck_two_p = []
    truck_two_a = []
    i = 0
    while i < len(packages):
        p = packages[i]
        if p.notes == 'Can only be on truck 2':
            package = packages.pop(i)
            truck_two_p.append(package)
            truck_two_a.append(package.address)
        i += 1

    j = 0
    while j < len(packages):
        p = packages[j]
        if p.address in truck_two_a or p:
            truck_two_p.append(packages.pop(j))
        j += 1

    print(f"truck two len: {len(truck_two_p)}")

    return truck


def load_truck_three(packages: list[Package], truck: Truck) -> Truck:
    pass
