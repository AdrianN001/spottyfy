from spoti.artist import Artist
from spoti.song import Song


class SearchResultSong(Song):
    added_at: str

    def __init__(self, title: str,
                 artists: list[Artist],
                 album_name: str,
                 duration_sec: int,
                 uri: str,
                 popularity: int,
                 preview_url: str):
        super().__init__(title ,artists, album_name, duration_sec, uri)
        self.popularity = popularity
        self.preview_url = preview_url
