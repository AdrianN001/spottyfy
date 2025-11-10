from lyrics.Lyric import Lyric
from spoti.artist import Artist
from spoti.song import Song
from typing import Union

class PlaybackSong(Song):
    progress_sec: int
    isPlaying: bool

    progress_ms: int
    album_image_url: str

    def __init__(self, title: str, 
                 artists: list[Artist], 
                 album_name: str, 
                 duration_sec: int, 
                 uri: str, 
                 progress_sec: int, 
                 isPlaying: bool, 
                 progress_ms: int,
                 album_image_url: str,
                 ):
        super().__init__(title ,artists, album_name, duration_sec, uri)
        self.progress_sec = progress_sec
        self.isPlaying = isPlaying
        self.progress_ms = progress_ms
        self.album_image_url = album_image_url

