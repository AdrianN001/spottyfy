import threading
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.timer import Timer
from textual.widgets import Footer
from typing import Union
from lyrics.LyricsDatabase import LyricsDatabase
from spoti import SpotifyClient, PlaybackSong
from tui.CurrentSongView import CurrentSongView
from tui.LyricContainer import LyricContainer
from tui.PlaylistTable import PlaylistTable
from .PlaybackBar import PlaybackBar

class GraphicClient(App):
    CSS = """
    PlaybackBar {
        width: 100%;
        height: 3;
        padding: 1;
    }

    PlaylistTable {
        width: 60%;
        height: 90%;
        padding: 1;
        border: round #1DB954;
        background: #111111;
        color: #dddddd;
    }

    PlaylistTable > .datatable--cursor {
        background: #1DB954;
        color: black;
        text-style: bold;
    }

    #lyric_container {
        layer: overlay;
        dock: bottom;
        height: 12;
        padding: 1 2;
        border: round #1DB954;
        background: rgba(0, 0, 0, 0.92);
        color: #1DB954;
        text-align: center;
        content-align: center middle;
        display: none;
    }
    CurrentSongView{
        width:30%;
    }
    """

    BINDINGS = [
        ("v", "toggle_playback", "Play/Pause"),
        ("n", "next_song", "Next"),
        ("b", "previous_song", "Back"),
        ("l", "toggle_lyrics", "Toggle Lyrics")
    ]

    spotify_client: SpotifyClient
    playback_bar: PlaybackBar
    playlist_table: PlaylistTable
    lyric_container: LyricContainer
    
    current_playback_song: Union[PlaybackSong, None]
    
    playback_refresh_timer: Timer
    lyrics_refresh_timer: Timer

    lyrics_db: LyricsDatabase
    
    def __init__(self):
        super().__init__()
        self.is_active = True
        self.current_playback_song = None
        self.lyrics_db = LyricsDatabase()

    def compose(self) -> ComposeResult:
        yield Horizontal(
            CurrentSongView(id="current_song"),

            PlaylistTable(id="playlist_table")
            )
        yield PlaybackBar(id="playback_bar")
        
        yield Footer()
        
        self.lyric_container = LyricContainer(id="lyric_container")
        yield self.lyric_container

    def on_mount(self) -> None:
        self.playback_bar = self.query_one("#playback_bar", PlaybackBar)
        self.playlist_table = self.query_one("#playlist_table", PlaylistTable)

        self.lyric_container.update_content("content")

        favourites = self.spotify_client.fetch_favorite_songs(50)
        if favourites == None:
            raise Exception("Saved cant be loadad.")
        self.playlist_table.load_new_songs(favourites, isSavedSongs=True)
        self.playlist_table.attach_spotify_client(self.spotify_client)

        self.playback_refresh_timer = self.set_interval(2, self.update_playback_bar)
        self.lyrics_refresh_timer = self.set_interval(0.5, self.update_lyric_container) 

    def action_toggle_playback(self) -> None:
        self.spotify_client.toggle_playback()

    def action_next_song(self) -> None:
        self.spotify_client.skip()

    def action_previous_song(self) -> None:
        self.spotify_client.prev()

    def action_toggle_lyrics(self) -> None:
        # 🟢 Toggle visibility instead of disabling
        self.lyric_container.display = not self.lyric_container.display
    
    def update_playback_bar(self) -> None:
        current_song = self.spotify_client.fetch_current_song()
        if current_song is None:
            return

        self.playback_bar.isActive = current_song.isPlaying


        if self.current_playback_song != current_song or self.current_playback_song is None:
            
            self.spotify_client.current_lyric = None

            self.current_playback_song = current_song
            self.playback_bar.set_new_song(current_song)
            self.playback_bar.completed_seconds = 0

            self.start_lyrics_fetch_in_backgrnd()
            self.update_current_song_view(current_song)
            
            self.playlist_table.update_table_by_new_song(current_song.uri)
        else: 
            self.playback_bar.completed_seconds = current_song.progress_sec

    def update_current_song_view(self, current_song: PlaybackSong) -> None:
        curr_song_view = self.query_one("#current_song", CurrentSongView)
        curr_song_view.update_current_song(current_song)
        
        next_song = self.spotify_client.get_next_song()
        if next_song != None:
            curr_song_view.update_next_song(next_song) 

    def update_lyric_container(self) -> None:
        
        result = self.lyrics_db.get_song(self.spotify_client.current_song)

        if type(result) == str:
            self.lyric_container.update_content(result)

            self.lyric_container.border_title = self.lyric_container.border_subtitle = "" 
        
        elif type(result) != str and self.spotify_client.current_lyric == None:
            self.spotify_client.set_current_lyrics(result)
        else:
                # Update the Lyrics Bar
            self.lyric_container.border_title = f"| Now playing: {self.spotify_client.current_song.title} |"
            self.lyric_container.border_subtitle = f"| by: {','.join(x.name for x in self.spotify_client.current_song.artists)} |"


            current_line = self.spotify_client.current_lyric.get_line(
                                    self.spotify_client.current_song.progress_ms
                                )
                
            if current_line != None:
                self.lyric_container.update_content(f"🎵 🎶 [white]{current_line.content}[/white] 🎵 🎶" )                           
            else:
                self.lyric_container.update_content("🎵 🎶 🎵 🎶")



    def start_lyrics_fetch_in_backgrnd(self) -> None:
        thread = threading.Thread(
                target=self.lyrics_db.fetch_in_background,
                args=(self.spotify_client.current_song,)
                )
        thread.start()

    def attach_spotify_client(self, client: SpotifyClient) -> None:
        self.spotify_client = client
  
