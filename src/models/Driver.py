class Driver:
    def __init__(self):
        self.available: bool = True

    def set_availability(self, available: bool = True) -> None:
        self.available = available
