class Driver:
    def __init__(self):
        self.available = True

    def __setitem__(self, key, value):
        self[key] = value
