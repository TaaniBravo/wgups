from models.Driver import Driver


class DriverPool:
    def __init__(self):
        self.pool = [
            Driver(),
            Driver()
        ]

    def enqueue_driver(self):
        return self.pool.pop()

    def add_driver_to_pool(self, driver: Driver):
        self.pool.append(driver)

