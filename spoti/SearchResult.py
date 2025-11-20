

from typing import Union
from spoti.Playlist import Playlist
from spoti.SearchResultSong import SearchResultSong
from spoti.artist import Artist

class SearchResult:
    tracks: Union[list[SearchResultSong], None]
    playlists: Union[list[Playlist], None]

    def __init__(self, q: str, raw_response: dict) -> None:
        self.q = q
        self.tracks = self.try_to_parse_tracks(raw_response)
        self.playlists = self.try_to_parse_playlists(raw_response)


    def try_to_parse_tracks(self, raw_response: dict) -> Union[list[SearchResultSong], None]:
        if "tracks" not in raw_response: return None

        raw_tracks = raw_response["tracks"]["items"]

        tracks = []

        for raw_track in raw_tracks:
            
            tracks.append(
                     SearchResultSong(
                        raw_track["name"],
                        [Artist(x) for x in raw_track["artists"]],
                        raw_track["album"]['name'],
                        raw_track["duration_ms"] / 1000,
                        raw_track['uri'],

                        raw_track["popularity"],
                        raw_track["preview_url"]
                        )
                    )

        return tracks

    def try_to_parse_playlists(self, raw_response: dict) -> Union[list[Playlist], None]:
        if "playlists" not in raw_response: return None

        raw_playlists = raw_response["playlists"]["items"]

        return [Playlist(x) for x in raw_playlists if x != None]

