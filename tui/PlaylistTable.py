

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
                " ",
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
                    " ",
                    str(indx+1),
                    song.title,
                    ",".join(x.name for x in song.artists[:2]),
                    song.album_name,
                    song.duration_formatted,
                    key=song.uri
                    )

    def update_table_by_new_song(self, song_uri: str) -> None:
        coll_key = [ key for key,value in self.columns.items() if value.width == 1 and value.content_width == 1][0]

        try:
            if hasattr(self, "_current_song_uri") and self._current_song_uri is not None:
                self.update_cell(self._current_song_uri, coll_key, " ")
            self._current_song_uri = ""

            self.update_cell(song_uri, coll_key, "▶")

            self._current_song_uri = song_uri
        except Exception:
            return

    async def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None: 
        song_uri = str(event.row_key.value)  
        row_data = self.get_row(song_uri) 

        song_index = int(row_data[1]) - 1

        
        if song_uri == None:
            return

        if self.isSavedSong:
            self.spotify_client.play_song_from_saved(song_index)
        else:
            self.spotify_client.play_song_from_playlist(self.context_uri, song_uri)
        
        self.update_table_by_new_song(song_uri)

