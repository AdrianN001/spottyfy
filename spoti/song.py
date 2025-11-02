

class Song:
    
    title: str
    artists: list[str]

    album_name: str

    duration_sec: int

    uri: str

    def __init__(self, title: str, artists: list[str], album_name: str, duration_sec: int, uri: str) -> None:
        self.title = title
        self.artists = artists.copy()
        self.album_name = album_name
        self.duration_sec = duration_sec
        self.uri = uri

    @property
    def duration_formatted(self) -> str:
        minute,seconds = divmod(int(self.duration_sec), 60)
        return f"{minute:02d}:{seconds:02d}"

    def __eq__(self, other) -> bool:
        if isinstance(other, Song):
            return other.uri == self.uri
        return False

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
