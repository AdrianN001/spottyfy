

from textual.widgets import DataTable, Static

from spoti.client import SpotifyClient
from spoti.playlist_song import PlayListSong



class PlaylistTable(DataTable):

    spotify_client: SpotifyClient
    context_uri:    str
    isSavedSong:    bool


    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.cursor_background_priority = "css"
        self.cursor_foreground_priority = "css"

        self.setup_collums()
        self.cursor_type = "row"
        self.zebra_stripes = False
        self.fixed_rows = 0
        self.show_header = True
        self.border_title = "| Saved Songs |"        


    def attach_spotify_client(self, spoti_client: SpotifyClient) -> None:
        self.spotify_client = spoti_client

    def setup_collums(self) -> None:
        self.clear(columns=True)

        self.add_columns(
                "#",
                "Titel",
                "Artist",
                "Album",
                "Length"
                )

    def load_new_songs(self, songs: list[PlayListSong], context_uri: str = "", isSavedSongs: bool = True) -> None: 
        self.clear()

        if context_uri == "" and isSavedSongs == False:
            return None

        self.context_uri = context_uri
        self.isSavedSong = isSavedSongs

        for indx, song in enumerate(songs):    
            self.add_row(
                    str(indx+1),
                    song.title,
                    ",".join(song.artists[:2]),
                    song.album_name,
                    song.duration_formatted,
                    key=song.uri
                    )




    async def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        row_key = event.row_key
        row_data = self.get_row(row_key)

        songIndex = int(row_data[0])-1
        songUri   = row_key.value
        
        if self.isSavedSong:
            self.spotify_client.play_song_from_saved(songIndex)
        else:
            self.spotify_client.play_song_from_playlist(self.context_uri, songUri)

