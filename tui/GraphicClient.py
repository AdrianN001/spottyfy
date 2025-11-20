from re import search
import threading
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.timer import Timer
from textual.widgets import Footer, Header
from typing import Union
from diary.diary import Diary
from lyrics.LyricsDatabase import LyricsDatabase
from spoti import SpotifyClient, PlaybackSong
from tui.CurrentSongView import CurrentSongView
from tui.DebugStats import DebugStatsWidget
from tui.LyricContainer import LyricContainer
from tui.PlaylistTable import PlaylistTable
from tui.SearchBar import SearchBar
from tui.SearchResultPanel import SearchResultPanel
from .PlaybackBar import PlaybackBar

class GraphicClient(App):
    CSS_PATH="../style/GraphicClient.tcss"

    BINDINGS = [
        ("v", "toggle_playback", "Play/Pause"),
        ("n", "next_song", "Next"),
        ("b", "previous_song", "Back"),
        ("l", "toggle_lyrics", "Toggle Lyrics"),
        ("d", "toggle_debug", "Toggle Debug")
    ]

    spotify_client: SpotifyClient
    playback_bar: PlaybackBar
    playlist_table: PlaylistTable
    lyric_container: LyricContainer
    
    current_playback_song: Union[PlaybackSong, None]
    
    playback_refresh_timer: Timer
    lyrics_refresh_timer: Timer

    lyrics_db: LyricsDatabase

    diary: Diary 
    
    def __init__(self):
        super().__init__()
        self.is_active = True
        self.current_playback_song = None
        self.lyrics_db = LyricsDatabase()

        self.diary = Diary()

        self.title = "spoTTYfy" 

    def compose(self) -> ComposeResult:
        yield Header(
                show_clock=True,
                id="header",
                )

        """ MAIN """
        yield Horizontal(
            CurrentSongView(id="current_song"),

            Vertical(
                PlaylistTable(id="playlist_table"),
                SearchBar(id="search_bar"),
                id="playlist_search_container"
                ),
            id="main_container"
            )

        yield PlaybackBar(id="playback_bar")
        
        yield Footer()
       
        """ Overlays """
        yield SearchResultPanel(id="search_result_panel")
        
        self.lyric_container = LyricContainer(id="lyric_container")
        yield self.lyric_container

        yield DebugStatsWidget(id="debug_stat_widget")

    def on_mount(self) -> None:
        self.playback_bar = self.query_one("#playback_bar", PlaybackBar)
        self.playlist_table = self.query_one("#playlist_table", PlaylistTable)
        self.debug_stat_widget = self.query_one("#debug_stat_widget", DebugStatsWidget)
        self.search_bar = self.query_one("#search_bar", SearchBar)
        self.search_result_panel = self.query_one("#search_result_panel", SearchResultPanel)

        self.search_bar.attach_spotify_client(self.spotify_client)
        self.search_bar.attach_diary(self.diary)
        self.search_result_panel.attach_diary(self.diary)
        self.search_result_panel.attach_spotify_client(self.spotify_client)

        self.search_result_panel.attach_playlist_table(self.playlist_table)
        self.search_bar.attach_result_panel(self.search_result_panel)

        self.debug_stat_widget.attach_spoti_usage_manager(
                self.spotify_client.usage_manager
                )

        self.debug_stat_widget.attach_spoti_profile(
                self.spotify_client.fetch_user_profile()
                )
        
        self.debug_stat_widget.attach_diary(
                self.diary
                )

        favourites = self.spotify_client.fetch_favorite_songs(50)
        if favourites == None:
            raise Exception("Saved cant be loadad.")

        self.playlist_table.load_new_songs(favourites, isSavedSongs=True)
        self.playlist_table.attach_spotify_client(self.spotify_client)

        self.playback_refresh_timer = self.set_interval(2, self.update_playback_bar)
        self.lyrics_refresh_timer = self.set_interval(0.1, self.update_lyric_container) 

    ## ACTIONS

    def action_toggle_playback(self) -> None:
        self.spotify_client.toggle_playback()

    def action_next_song(self) -> None:
        self.spotify_client.skip()

    def action_previous_song(self) -> None:
        self.spotify_client.prev()

    def action_toggle_lyrics(self) -> None:
        self.lyric_container.display = not self.lyric_container.display

    def action_toggle_debug(self) -> None:
        self.debug_stat_widget.display = not self.debug_stat_widget.display

        self.debug_stat_widget.isActive = self.debug_stat_widget.display


    """ Timer callback methods """

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

        self.diary.info(
                "start_lyrics_fetch_in_backgrnd()", 
                f"Starting lyrics fetch for {self.spotify_client.current_song.title} in a new thread.")

    def attach_spotify_client(self, client: SpotifyClient) -> None:
        self.spotify_client = client
        client.attach_diary(self.diary)
  
