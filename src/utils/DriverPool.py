from models.Driver import Driver


class DriverPool:
    def __init__(self, drivers: list[Driver]):
        self.drivers = drivers

    def get_available_driver(self) -> Driver:
        return self.drivers.pop()

    def assign_driver(self):
        driver: Driver = self.get_available_driver()
        driver.set_availability(False)
        return driver

    def add_driver_to_pool(self, driver: Driver):
        driver.set_availability(True)
        self.drivers.append(driver)
