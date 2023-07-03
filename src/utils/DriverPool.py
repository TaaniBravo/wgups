from models.Driver import Driver


class DriverPool:
    def __init__(self, drivers: list[Driver]):
        self.drivers = drivers

    def get_available_driver(self) -> Driver:
        """
        Returns the first available driver in the pool
        :return:
        """
        return self.drivers.pop()

    def assign_driver(self):
        """
        Assigns a driver to a truck
        :return:
        """
        driver: Driver = self.get_available_driver()
        driver.set_availability(False)
        return driver

    def add_driver_to_pool(self, driver: Driver):
        """
        Adds a driver to the pool
        :param driver:
        :return:
        """
        driver.set_availability(True)
        self.drivers.append(driver)
