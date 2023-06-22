import sys
from math import floor
from typing import Any


class Location:
    def __init__(self, id: int, name: str, address: str) -> None:
        self.id = id
        self.name = name
        self.address = address
        self.distance: float = sys.maxsize
        self.pred_loc = None

    def __getitem__(self, item) -> Any:
        return self[item]

    def __setitem__(self, key: Any, value: Any) -> None:
        self[key] = value

    @staticmethod
    def find_by_address(locations: list, address: str) -> Any:
        for loc in locations:
            if address == loc.address:
                return loc
        return None

    @staticmethod
    def find_by_id(packages: list, id: int):
        """Will do a binary search on the packages to find the package with the
        matching ID. Assumes list is sorted by ID."""
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
