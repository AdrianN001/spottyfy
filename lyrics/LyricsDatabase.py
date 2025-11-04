from config.lyric import lyric_cahce_file_exists, open_lyric_cache_file, write_lyric_cache_file
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

    def search_song_from_web(self, current_song: PlaybackSong) -> Union[Lyric, None]:
        lyric = search_for_lyric(current_song.artists[0], current_song.title, current_song.uri)
        if lyric != None:
            write_lyric_cache_file(lyric.to_parsable_content(), current_song.uri) 
        with self.mutex:
            self.container[current_song.uri] = lyric
            return lyric

    def search_song_from_disk(self,current_song: PlaybackSong) -> Union[Lyric, None]:
        if not lyric_cahce_file_exists(current_song.uri): 
            return None

        raw_lyric = open_lyric_cache_file(current_song.uri)
        if raw_lyric == None:
            return None

        parsed_lyric = Lyric.from_parsed_content(raw_lyric)

        with self.mutex:
            self.container[current_song.uri] = parsed_lyric
            return parsed_lyric

    def fetch_in_background(self, current_song: PlaybackSong) -> None:
        disk_result = self.search_song_from_disk(current_song)
        
        if disk_result == None:
            self.search_song_from_web(current_song)

    def get_song(self, current_song: PlaybackSong) -> Union[Lyric, str]:
        if current_song.uri in self.container:
            with self.mutex:
                lyric = self.container[current_song.uri]
                if lyric == None:
                    return "No lyrics found."
                return lyric

        return "Fetching..."
