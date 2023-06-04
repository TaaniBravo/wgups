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
        notes: str,
    ) -> None:
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes

    def update_status(self, status: str):
        pass

    def get_current_status(self) -> str:
        return self.status
