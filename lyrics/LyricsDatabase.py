

from lyrics.Lyric import Lyric
from lyrics.search import search_for_lyric
from spoti.playback_song import PlaybackSong
from typing import Union
from threading import Lock

class LyricsDatabase:

    container: dict[str, Union[Lyric, None]]
    mutex = Lock()

    def __init__(self) -> None:
        self.container = dict()

    def search_song(self, current_song: PlaybackSong) -> Union[Lyric, None]:
        lyric = search_for_lyric(current_song.artists[0], current_song.title, current_song.uri)
        with self.mutex:
            self.container[current_song.uri] = lyric
            return lyric

    def fetch_in_background(self, current_song: PlaybackSong) -> None:
        self.search_song(current_song)

    def get_song(self, current_song: PlaybackSong) -> Union[Lyric, str]:
        if current_song.uri in self.container:
            with self.mutex:
                lyric = self.container[current_song.uri]
                if lyric == None:
                    return "No lyrics found."
                return lyric

        return "Fetching..."
