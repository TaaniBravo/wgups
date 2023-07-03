class Location:
    def __init__(self, id: int, name: str, address: str):
        self.id: int = id
        self.name: str = name
        self.address: str = address
        self.distance: float = float('inf')

    def __setitem__(self, key, value) -> None:
        self[key] = value

    @staticmethod
    def find_by_address(locations: list, address: str):
        for location in locations:
            if location.address == address:
                return location
        return None
