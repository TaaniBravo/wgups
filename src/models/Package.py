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
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = 'At the hub'

    def __setitem__(self, key: str, value: Any):
        """Sets a value an instances of Package's properties"""
        self[key] = value

    def __getitem__(self, item: Any):
        """Returns an instances of Package's properties"""
        return self[item]

    @staticmethod
    def find_by_id(pois: list, id: int):
        """Will do a binary search on the packages to find the package with the
        matching ID. Assumes list is sorted by ID."""
        low = 0
        high = len(pois)

        while low < high:
            midpoint = floor(low + (high - low) / 2)
            current_poi = pois[midpoint]
            if current_poi.id == id:
                return current_poi
            elif id > current_poi.id:
                low = midpoint + 1
            else:
                high = midpoint

        return None
