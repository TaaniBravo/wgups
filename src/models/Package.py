from calendar import timegm
from datetime import datetime
from math import floor
from typing import Any


class Package(object):
    """TODO: Write documentation"""

    status: str

    def __init__(
            self,
            id: int,
            address: str,
            city: str,
            state: str,
            zip: int,
            deadline: str,
            weight: int,
            notes: str or None,
    ) -> None:
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        today = datetime.today()
        if deadline != "EOD":
            split_dl = deadline.split(":")
            hours = int(split_dl[0])
            minutes = int(split_dl[1])
            secs = int(split_dl[2])
            dl_datetime = datetime(today.year, today.month, today.day, hours, minutes, secs)
            self.deadline = dl_datetime
        else:
            self.deadline = datetime(today.year, today.month, today.day, 23, 59, 59)
        self.weight = weight
        self.notes = notes
        self.status = 'At the hub'
        self.delivery_time = None
        self.truck_id: str or None = None

    def __setitem__(self, key: str, value: Any):
        """Sets a value an instances of Package's properties"""
        self[key] = value

    def __getitem__(self, item: Any):
        """Returns an instances of Package's properties"""
        return self[item]

    @staticmethod
    def find_by_address(packages: list, address: str) -> list:
        return list(filter(lambda p: p.address == address, packages))

    @staticmethod
    def packages_have_deadline(packages: list) -> bool:
        """

        :param packages:
        :return:
        """
        for package in packages:
            if package.deadline != "EOD":
                return True

        return False

    @staticmethod
    def find_by_id(packages: list, id: int):
        """
        Will do a binary search on the packages to find the package with the
        matching ID. Assumes list is sorted by ID.
        Time Complexity: O(logn)
        """
        low = 0
        high = len(packages)

        while low < high:
            midpoint = floor(low + (high - low) / 2)
            current_package = packages[midpoint]
            if current_package.id == id:
                return current_package
            elif id > current_package.id:
                low = midpoint + 1
            else:
                high = midpoint

        return None

    def update(self, status: str, delivery_time=None):
        """
        Updates the status and delivery time of the package.
        Time Complexity: O(1)
        """
        self.status = status
        if isinstance(delivery_time, datetime):
            self.delivery_time = delivery_time

    def __str__(self):
        """
        Returns a user-friendly string of the package.
        Time Complexity: O(1)
        """
        if isinstance(self.deadline, str):
            delivered_on_time = True
        elif self.delivery_time is None:
            delivered_on_time = False
        else:
            delivered_on_time = timegm(self.deadline.timetuple()) > timegm(self.delivery_time.timetuple())
        return "--------\n" \
               f"Package ID: {self.id}\n" \
               f"Truck ID: {self.truck_id}\n" \
               f"Status: {self.status}\n" \
               f"Deadline: {self.deadline}\n" \
               f"Delivery Time: {self.delivery_time}\n" \
               f"Delivered on time: {delivered_on_time}\n" \
               "--------\n"
