

class Artist:

    name: str
    _id: str
    def __init__(self, artist_object: dict) -> None:
        self.name = artist_object['name']
        self._id = artist_object['id']
