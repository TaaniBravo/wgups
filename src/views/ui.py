from datetime import datetime

from inquirer import prompt, List, Text

from models.Package import Package
from models.Truck import Truck
from utils.time import get_today_datetime, get_eod


def print_welcome_message():
    print("Welcome to WGUPS")


def print_total_milage(trucks: list[Truck]):
    total_milage = 0
    for truck in trucks:
        total_milage += truck.accumulated_distance
    print(f"Total distance traveled: {total_milage} miles")


def view_all_packages(packages: list[Package]):
    answers = prompt([
        Text('time', 'Enter a time to view the status of all packages at that time (HH:MM:SS). Leave empty for EOD')
    ])
    try:
        time = get_eod() if answers['time'] == '' else datetime.strptime(answers['time'], '%H:%M:%S')
        curr_time = get_today_datetime(time.hour, time.minute, time.second)
        for p in packages:
            p.print(curr_time)
        print()
    except ValueError:
        print("Invalid time format. Please try again.")
        return


def filter_by_id(packages: list[Package], time: datetime):
    answers = prompt([
        Text('id', 'Enter a package ID')
    ])
    try:
        id = int(answers['id'])
        package = Package.find_by_id(packages, id)
        if package is None:
            print(f"Package with ID {id} not found")
            return
        package.print(time)
        print()
    except ValueError:
        print("Invalid ID. Please try again.")
        filter_by_id(packages, time)


def filter_by_address(packages: list[Package], time: datetime):
    choices = list(set([p.address for p in packages]))
    answers = prompt([
        List('address', message="Select an address", choices=choices)
    ])
    address = answers['address']
    filtered_packages = Package.find_by_address(packages, address)
    for p in filtered_packages:
        p.print(time)
    print()


def filter_by_deadline(packages: list[Package], time: datetime):
    choices = list(set([p.deadline for p in packages]))
    answers = prompt([
        List('deadline', message="Select a deadline", choices=choices)
    ])
    deadline = answers['deadline']
    for p in packages:
        if p.deadline == deadline:
            p.print(time)
    print()


def filter_by_city(packages: list[Package], time: datetime):
    choices = list(set([p.city for p in packages]))
    answers = prompt([
        List('city', message="Select a city", choices=choices)
    ])
    city = answers['city']
    for p in packages:
        if p.city == city:
            p.print(time)
    print()


def filter_by_zip_code(packages: list[Package], time: datetime):
    choices = list(set([p.zip_code for p in packages]))
    answers = prompt([
        List('zip_code', message="Select a zip code", choices=choices)
    ])
    zip_code = answers['zip_code']
    for p in packages:
        if p.zip_code == zip_code:
            p.print(time)
    print()


def filter_by_weight(packages: list[Package], time: datetime):
    answers = prompt([
        Text('min', 'Enter a min weight'),
        Text('max', 'Enter a max weight')
    ])
    try:
        min_weight = float(answers['min'])
        max_weight = float(answers['max'])
        for p in packages:
            if min_weight <= p.weight <= max_weight:
                p.print(time)
    except ValueError:
        print("Invalid weight values. Please try again.")
        filter_by_weight(packages, time)


def filter_by_status(packages: list[Package], time: datetime):
    choices = ['At Hub', 'En Route', 'Delivered']
    answers = prompt([
        List('status', message="Select a status", choices=choices)
    ])
    for p in packages:
        if answers['status'] in p.determine_status(time):
            p.print(time)
    print()


def filter_packages_by_field(packages: list[Package]):
    answers = prompt([
        List('action', message="Select a package field to filter by",
             choices=['ID', 'Address', 'Deadline', 'City', 'Zip Code', 'Weight', 'Status', 'Quit']),
        Text('time', 'Enter a time (HH:MM:SS). Leave empty for EOD')
    ])
    try:
        time = get_eod() if answers['time'] == '' else datetime.strptime(answers['time'], '%H:%M:%S')
        curr_time = get_today_datetime(time.hour, time.minute, time.second)
        if answers['action'] == 'ID':
            filter_by_id(packages, curr_time)
        elif answers['action'] == 'Address':
            filter_by_address(packages, curr_time)
        elif answers['action'] == 'Deadline':
            filter_by_deadline(packages, curr_time)
        elif answers['action'] == 'City':
            filter_by_city(packages, curr_time)
        elif answers['action'] == 'Zip Code':
            filter_by_zip_code(packages, curr_time)
        elif answers['action'] == 'Weight':
            filter_by_weight(packages, curr_time)
        elif answers['action'] == 'Status':
            filter_by_status(packages, curr_time)
        elif answers['action'] == 'Quit':
            quit()
    except ValueError:
        print("Invalid time format. Please try again.")
        filter_packages_by_field(packages)


def ui(trucks: list[Truck], packages: list[Package]):
    print_welcome_message()
    print_total_milage(trucks)
    while True:
        answers = prompt([
            List('action', message="What would you like to do?",
                 choices=['View All Packages', 'Filter Packages by Field', 'Quit'])
        ])

        if answers['action'] == 'View All Packages':
            view_all_packages(packages)
        elif answers['action'] == 'Filter Packages by Field':
            filter_packages_by_field(packages)
        elif answers['action'] == 'Quit':
            quit()
