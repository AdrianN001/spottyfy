from spoti.song import Song


class PlaybackSong(Song):
    progress_sec: int

    def __init__(self, title: str, artists: list[str], album_name: str, duration_sec: int,uri: str, progress_sec: int):
        super().__init__(title ,artists, album_name, duration_sec, uri)
        self.progress_sec = progress_sec
