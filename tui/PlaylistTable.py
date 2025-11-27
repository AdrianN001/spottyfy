

from textual.widgets import DataTable, Static

from diary.diary import Diary
from spoti.Playlist import Playlist
from spoti.client import SpotifyClient
from spoti.playlist_song import PlayListSong



class PlaylistTable(DataTable):

    savedSongs: list[PlayListSong]
    playlist:   Playlist

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

    def attach_diary(self, diary: Diary) -> None:
        self.diary = diary

    def setup_collums(self) -> None:
        self.clear(columns=True)
        
        self.add_column(" ", key="pointer_col", width=1)
        self.add_column("#", key="index_col", width=2)
        self.add_column("Titel", key="titel_col", width=30)
        self.add_column("Artist", key="artist_col", width=25)
        self.add_column("Album", key="album_col", width=25)
        self.add_column("Length", key="length_col", width=10)

    def load_new_songs(self, songs: list[PlayListSong], context_uri: str = "", isSavedSongs: bool = True) -> None: 
        self.clear()
   
        self.savedSongs = songs
        self.playlist = None
        self.border_title = "| Saved Songs |"
    
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

    def load_playlist(self, playlist: Playlist) -> None:
        self.clear()

        self.playlist = playlist
        self.isSavedSong = False

        self.border_title = f"| {playlist.name} |"

        for indx, song in enumerate(playlist.tracks):   
            try:
                self.add_row(
                    " ",
                    str(indx+1),
                    song.title,
                    ",".join(x.name for x in song.artists[:2]),
                    song.album_name,
                    song.duration_formatted,
                    key=song.uri
                    )
            except Exception:
                # Duplicate
                continue
        
        self.focus()


    def search_from_playlist(self, query: str) -> None:
        self.clear()

        prev_border_title = self.border_title.replace("|","")
        
        if "Searching" in prev_border_title:
            prev_border_title = prev_border_title.split("Searching")[0]
        
        prev_border_title = prev_border_title.strip()

        new_border_title = "| " + prev_border_title + f" [#aaaaaa] Searching: {query} [/#aaaaaa]" + " |"
        
        self.border_title = new_border_title
        
        indx = 0
        for song in self.savedSongs if self.isSavedSong else self.playlist.tracks:
            self.diary.info("search_from_playlist()", f"{song.title.lower()=} {query.lower()=}")

            self.diary.info("search_from_playlist()", f"{song.album_name.lower()=} {query.lower()=}")
            
            if query.lower() not in song.title.lower() \
                    and query.lower() not in song.album_name.lower() \
                    and not any(query.lower() in artist.name.lower() for artist in song.artists): 
                        continue

            try:
                self.add_row(
                    " ",
                    str(indx+1),
                    song.title,
                    ",".join(x.name for x in song.artists[:2]),
                    song.album_name,
                    song.duration_formatted,
                    key=song.uri
                    )
                indx += 1
            except Exception:
                # duplicate
                continue
        self.focus()




    def clear_search(self) -> None:
        self.clear()

        prev_border_title = self.border_title.replace("|","")
        
        if "Searching" in prev_border_title:
            prev_border_title = prev_border_title.split("Searching")[0]
        
        self.border_title = prev_border_title.strip()

        
        for indx, song in enumerate(self.savedSongs if self.isSavedSong else self.playlist.tracks):    
            try:
                self.add_row(
                    " ",
                    str(indx+1),
                    song.title,
                    ",".join(x.name for x in song.artists[:2]),
                    song.album_name,
                    song.duration_formatted,
                    key=song.uri
                    )
            except exception:
                # duplicate
                continue
        self.focus()


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
        elif self.playlist != None:
            self.spotify_client.play_song_from_playlist(self.playlist.playlist_id, song_uri)
        
        self.update_table_by_new_song(song_uri)

