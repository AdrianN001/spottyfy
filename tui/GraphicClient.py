from textual.app import App, ComposeResult
from textual.timer import Timer
from textual.widget import Widget
from typing import Union

from spoti import SpotifyClient, PlaybackSong
from tui.PlaylistTable import PlaylistTable
from .PlaybackBar import PlaybackBar

class GraphicClient(App):
    CSS="""
    PlaybackBar {
        width: 100%;
        height: 3;
        padding: 1;
        content-align: center middle;

    }
    PlaylistTable{
        width: 80%;
        height: 90%;
        padding: 1;

        border: round green;
        background: #111111;
        color: #dddddd;
    }
    PlaylistTable > .datatable--cursor {
        background: #1DB954;
        color: black;
        text-style: bold;
    }

    """
    spotify_client: SpotifyClient
    playback_bar  : PlaybackBar
    playlist_table: PlaylistTable

    current_playback_song: Union[PlaybackSong,None]

    # Timers
    playback_refresh_timer: Timer

    def __init__(self):
        super().__init__()
        self.is_active = True
        self.current_playback_song = None


    def compose(self) -> ComposeResult:
        yield PlaylistTable(id="playlist_table")
        yield PlaybackBar(id="playback_bar") 

    def on_mount(self) -> None:
        self.playback_bar: PlaybackBar = self.query_one("#playback_bar")
        self.playlist_table: PlaylistTable = self.query_one("#playlist_table")


        favourites = self.spotify_client.fetch_favorite_songs(100)
        self.playlist_table.load_new_songs(favourites, isSavedSongs=True)

        self.playlist_table.attach_spotify_client(self.spotify_client)

        self.playback_refresh_timer = self.set_interval(2, self.update_playback_bar)

    def update_playback_bar(self) -> None:
        
        current_song = self.spotify_client.fetch_current_song()
        if current_song is None:
            return

        if self.current_playback_song != current_song or self.current_playback_song == None:
            self.current_playback_song = current_song

            self.playback_bar.set_new_song(current_song)
            self.playback_bar.completed_seconds = 0
        else:
            self.playback_bar.completed_seconds = current_song.progress_sec


    def attach_spotify_client(self, client: SpotifyClient) -> None:
        self.spotify_client = client
   
