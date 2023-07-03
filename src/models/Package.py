from datetime import datetime

from models.Location import Location


class Package:
    def __init__(self, id: int, address: str, city: str, state: str, zip_code: str, deadline: datetime, weight: float,
                 notes: str or None, location: Location, delayed: bool = False):
        self.id: int = id
        self.address: str = address
        self.city: str = city
        self.state: str = state
        self.zip_code: str = zip_code
        self.deadline: datetime = deadline
        self.weight: float = weight
        self.notes: str or None = notes
        self.status: str = 'At Hub'
        self.location: Location = location
        self.delivery_time: datetime or None = None
        self.en_route_time: datetime or None = None
        self.delayed: bool = delayed
        self.delayed_datetime: datetime or None = None
        self.truck_id: int or None = None

    def __setitem__(self, key, value):
        self[key] = value

    def __getitem__(self, item):
        return self[item]

    @staticmethod
    def find_by_id(packages: list, id: int):
        """
        Binary search for a package by id
        Time complexity: O(log n)
        Space complexity: O(1)
        """
        low = 0
        high = len(packages)
        while low < high:
            mid = (low + high) // 2
            if packages[mid].id == id:
                return packages[mid]
            elif packages[mid].id < id:
                low = mid + 1
            else:
                high = mid
        return None

    @staticmethod
    def find_by_address(packages: list, address: str):
        return_list = []
        for p in packages:
            if p.address == address:
                return_list.append(p)
        return return_list

    def determine_status(self, current_time: datetime) -> str:
        if current_time < self.en_route_time:
            return 'At Hub'
        elif self.en_route_time <= current_time < self.delivery_time:
            return 'En Route'
        elif current_time >= self.delivery_time:
            status = 'Delivered'
            if self.delivery_time < self.deadline:
                status += ' On Time'
            else:
                status += ' Late'
            status += f' at {self.delivery_time.strftime("%I:%M %p")}'
            return status

    def print(self, current_time: datetime):
        print(
            f'{self.id} | {self.address} | {self.deadline} | {self.city} | {self.state} | {self.zip_code} | {self.weight} | {self.determine_status(current_time)}')
