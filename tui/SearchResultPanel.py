from textual.containers import Center, Horizontal, Vertical
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Button, DataTable, Label, ListItem, ListView, Static
from diary import Diary
import diary
from spoti import playlist_song
from spoti.SearchResult import SearchResult
from spoti.client import SpotifyClient
from tui.PlaylistTable import PlaylistTable

class SearchResultPanel(Widget):
    DEFAULT_CSS="""
    DataTable{
        border: magenta round;
        height: 100%;
    }
    ListView{
        border: magenta round;
    }

    #top_container{
        height: 60%;
    }
    #main_container{
        width: 100%;
        height: 98%;
    }
   
    #tracks_list{
        width: 40%;
    }
    #playlist_list{
        width: 40%;
    }
    #artist_list{
        width: 20%;
    }
    """ 

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


    def on_key(self, event) -> None:
        if event.key == "e":
            self.display = False

    def load_search_result(self, result: SearchResult) -> None:
        self.display = True
        
        self.track_list.focus()
    
        self.track_list.clear()
        self.playlist_list.clear()
        self.artist_list.clear()
        
       
        tracks_list_width = 90
        for track in result.tracks:
            
            max_fire_str_len = 6
            fire_str = "🔥" * (track.popularity // 20 + 1)
            spacing = " "* (max_fire_str_len - len(fire_str))

            self.track_list.add_row(
                    track.title,
                    ", ".join([x.name for x in track.artists[:2]]),
                    f"{int(track.duration_sec / 60):02}:{int(track.duration_sec%60):02}",
                    f"{spacing}{fire_str}",
                    key=track.uri
                    )
      

        for playlist in result.playlists:
            
            self.playlist_list.add_row(
                    playlist.name,
                    playlist.owner_display_name,
                    playlist.track_number,
                    key=playlist.playlist_id
                    )


        self.border_title = f"[white]Results for: [/white][bold]{result.q}[/bold]"
        self.refresh()
    


    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(
                DataTable(id="tracks_list"),
                DataTable(id="playlist_list"),
                ListView(id="artist_list"), 
                id="top_container"
                ),
            Horizontal(
                ListView(id="album_list"),
                id="bottom_container"
                ),


            id="main_container"
        )
    def on_mount(self) -> None:
        self.track_list = self.query_one("#tracks_list", DataTable)
        self.playlist_list = self.query_one("#playlist_list", DataTable)
        self.artist_list = self.query_one("#artist_list", ListView)
            
        self.track_list.border_title = "|>Tracks:"
        self.playlist_list.border_title = "|> Playlists:"
        self.artist_list.border_title = "|> Artists:"

        self.init_tables()

    def init_tables(self) -> None:
        self.track_list.clear(columns=True)
        self.playlist_list.clear(columns=True)

        self.track_list.add_column("Titel", key="title", width=25)
        self.track_list.add_column("Artist", key="artist", width=25)
        self.track_list.add_column("Length", width=10) 
        self.track_list.add_column("Popularity", width=10)

        self.track_list.cursor_type="row"

        self.playlist_list.add_column("Name", key="name", width=35)
        self.playlist_list.add_column("Owner", key="owner", width=25)
        self.playlist_list.add_column("# of songs", key="songs", width=10)

        self.playlist_list.cursor_type="row"

    async def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        uri = str(event.row_key.value)  
        
        if ":track:" in uri:
            self.spotify_client.start_song(uri)
        elif ":playlist:":
            playlist = self.spotify_client.fetch_playlist(uri)
            if playlist != None:
                self.playlist_table.load_playlist(playlist)
                
                self.display = False

    def attach_diary(self, diary: Diary) -> None:
        self.diary = diary
    
    def attach_spotify_client(self, spoti: SpotifyClient) -> None:
        self.spotify_client = spoti

    def attach_playlist_table(self, playlist_table: PlaylistTable) -> None:
        self.playlist_table = playlist_table
