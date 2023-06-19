import csv

from models.Package import Package
from models.Location import Location
from utils.ChainingHashTable import ChainingHashTable
from utils.Graph import Graph


def get_packages(filename: str) -> ChainingHashTable:
    """Reads from the CSV file package.csv and returns a list of packages."""
    # Add the packages to a table based on the address. There are a total of 26 addresses.
    with open(filename, newline='') as package_file:
        reader = csv.reader(package_file, delimiter=',')
        packages = ChainingHashTable(26)
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
            packages.insert(package, address)

    return packages


def get_locations(filename: str) -> list[Location]:
    pois = []
    with open(filename, newline='') as address_file:
        reader = csv.reader(address_file, delimiter=',')
        for row in reader:
            id = int(row[0])
            name = row[1]
            address = row[2]
            poi = Location(id, name, address)
            pois.append(poi)

    return pois


def get_downtown_map(filename: str, poi_filename: str) -> Graph:
    """
    Reads a csv file and creates a Map (graph) of all POIs in downtown.
    Runs at O(nm^2). n being the amount of POIs and m^2 from having to iterate of the distance matrix.
    """
    downtown_map = Graph()
    pois = get_locations(poi_filename)
    with open(filename, newline='') as distance_file:
        reader = csv.reader(distance_file, delimiter=',')
        for i, row in enumerate(reader):
            for j, col in enumerate(row):
                if col == '':
                    continue
                distance = float(col)
                from_poi = pois[i]
                to_poi = pois[j]
                downtown_map.add_location(from_poi)
                if to_poi != from_poi:
                    downtown_map.add_location(to_poi)
                downtown_map.add_route(from_poi, to_poi, distance)

    return downtown_map
