import csv

from utils.Graph import Graph
from utils.time import get_today_datetime, get_eod
from models.Location import Location
from models.Package import Package


def get_packages_from_csv(filename: str, locations: list[Location]) -> list[Package]:
    """
    Reads a CSV file and returns a list of packages
    Time complexity: O(n)
    Space complexity: O(n)
    :param filename:
    :param locations:
    :return:
    """
    packages = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            if row[5] == 'EOD':
                deadline = get_eod()
            else:
                deadline_split = row[5].split(':')
                deadline = get_today_datetime(int(deadline_split[0]), int(deadline_split[1]))
            weight = float(row[6])
            notes = None if row[7] == 'None' else row[7]
            location = Location.find_by_address(locations, address)
            package = Package(id=id, address=address, city=city, state=state, zip_code=zip_code, deadline=deadline,
                              weight=weight, notes=notes, location=location)
            if package.id == 9:
                package.location = Location.find_by_address(locations, '410 S State St')
                package.delayed = True
                package.delayed_datetime = get_today_datetime(10, 20)
            packages.append(package)
    return packages


def get_locations_from_csv(filename: str) -> list[Location]:
    """
    Reads a CSV file and returns a list of locations
    Time complexity: O(n)
    Space complexity: O(n)
    :param filename:
    :return:
    """
    locations = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            id = int(row[0])
            name = row[1]
            address = row[2]
            locations.append(Location(id, name, address))
    return locations


def get_distances_from_csv(filename: str, locations: list[Location]) -> Graph:
    """
    Reads a CSV file and returns a graph of locations and their distances from each other
    Time complexity: O(n^2)
    Space complexity: O(n^2)
    :param filename:
    :param locations:
    :return:
    """
    graph = Graph()
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(reader):
            for j in range(0, len(row)):
                if row[j] == '':
                    continue
                from_location = locations[i]
                to_location = locations[j]
                distance = float(row[j])
                if from_location != to_location:
                    graph.add_vertex(to_location)
                graph.add_vertex(from_location)
                graph.add_undirected_edge(from_location, to_location, distance)
    return graph
