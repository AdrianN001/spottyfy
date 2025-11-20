

from typing import Union
from spoti.artist import Artist
from spoti.playlist_song import PlayListSong


class Playlist:

    raw_data: dict

    owner_display_name: str
    name: dict
    playlist_id: str
    track_number: int

    tracks: Union[list[PlayListSong], None]

    def __init__(self, raw_data: dict) -> None:
        self.raw_data = raw_data

        self.owner_display_name = raw_data["owner"]["display_name"]
        self.name = raw_data["name"]
        self.playlist_id = raw_data["uri"]
        self.track_number = raw_data["tracks"]["total"]

        self.tracks = Playlist.__try_to_parse_tracks(raw_data)


    @staticmethod
    def __try_to_parse_tracks(raw_data: dict) -> Union[list[PlayListSong], None]:
        if "items" not in raw_data["tracks"]: return None

        ret_list = []
        for raw_item in raw_data["tracks"]["items"]:
            track = raw_item["track"]
            added_at = raw_item["added_at"]
            ret_list.append(
                    PlayListSong(
                            track['name'],
                            [Artist(x) for x in track['artists']],
                            track['album']['name'],
                            track['duration_ms'] / 1000,
                            track['uri'],
                            added_at
                        )
                    )

        return ret_list


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"
