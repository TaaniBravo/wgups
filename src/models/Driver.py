class Driver:
    def __init__(self):
        self.available: bool = True

    def set_availability(self, available: bool = True) -> None:
        """
        Sets the availability of the driver
        :param available:
        :return:
        """
        self.available = available
