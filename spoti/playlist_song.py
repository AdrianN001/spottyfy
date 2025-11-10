from spoti.artist import Artist
from spoti.song import Song


class PlayListSong(Song):
    added_at: str

    def __init__(self, title: str,
                 artists: list[Artist],
                 album_name: str,
                 duration_sec: int,
                 uri: str,
                 added_at: str):
        super().__init__(title ,artists, album_name, duration_sec, uri)
        self.added_at = added_at.split("T")[0]
