import csv

from models.Package import Package
from models.Location import Location
from utils.ChainingHashTable import ChainingHashTable
from utils.Graph import Graph
from os import path

ROOT_DIR = path.join(path.dirname(path.abspath(__file__)), '../../')


def get_packages(filename: str) -> list[Package]:
    """Reads from the CSV file package.csv and returns a list of packages."""
    # Add the packages to a table based on the address. There are a total of 26 addresses.
    with open(path.join(ROOT_DIR, filename), newline='') as package_file:
        reader = csv.reader(package_file, delimiter=',')
        packages = []
        for row in reader:
            id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip = int(row[4])
            deadline = row[5]
            weight = int(row[6])
            notes = None if row[7] == 'None' else row[7]
            package = Package(id, address, city, state, zip, deadline, weight, notes)
            packages.append(package)

    return packages


def get_locations(filename: str) -> list[Location]:
    pois = []
    with open(path.join(ROOT_DIR, filename), newline='') as address_file:
        reader = csv.reader(address_file, delimiter=',')
        for row in reader:
            id = int(row[0])
            name = row[1]
            address = row[2]
            poi = Location(id, name, address)
            pois.append(poi)

    return pois


def get_downtown_map(filename: str, locations: list[Location]) -> Graph:
    """
    Reads a csv file and creates a Map (graph) of all POIs in downtown.
    Runs at O(nm^2). n being the amount of POIs and m^2 from having to iterate of the distance matrix.
    """
    downtown_map = Graph()
    with open(path.join(ROOT_DIR, filename), newline='') as distance_file:
        reader = csv.reader(distance_file, delimiter=',')
        for i, row in enumerate(reader):
            for j, col in enumerate(row):
                if col == '':
                    continue
                distance: float = float(col)
                from_loc: Location = locations[i]
                to_loc: Location = locations[j]
                downtown_map.add_location(from_loc)
                if to_loc != from_loc:
                    downtown_map.add_location(to_loc)
                downtown_map.add_route(from_loc, to_loc, distance)

    return downtown_map
