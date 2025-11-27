
from asyncio import Event
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.events import Enter
from textual.widgets import Input

from diary.diary import Diary
from spoti.SearchResult import SearchResult
from spoti.client import SpotifyClient
from tui.PlaylistTable import PlaylistTable
from tui.SearchResultPanel import SearchResultPanel


class SearchBar(Input):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.cursor_blink = False
        self.valid_empty = False
        self.placeholder="Search..."

    def attach_spotify_client(self, spotify_client: SpotifyClient) -> None:
        self.spotify_client = spotify_client

    def attach_diary(self, diary: Diary) -> None:
        self.diary = diary

    def attach_result_panel(self, panel: SearchResultPanel) -> None:
        self.result_panel = panel

    def attach_playlist_table(self, playlistTable: PlaylistTable) -> None:
        self.playlistTable = playlistTable

    def search_in_playlist(self, query: str) -> None:
        self.playlistTable.search_from_playlist(query)
    
    def clear_playlist_search(self) -> None:
        self.playlistTable.clear_search()

    def check_if_decorator_used(self, query: str) -> bool:
        if query.startswith("@local:"):
            q = query.replace("@local:","")
            if q == "":
                self.clear_playlist_search()
                return True
            self.search_in_playlist(q)
            return True
        return False

    def on_input_submitted(self, event: Input.Submitted) -> None:
        value = event.input.value
        event.input.value = ""
        value_processed = self.check_if_decorator_used(value)
        
        if value_processed: 
            return 

        self.diary.info("on_input_submitted()", f"Search started: Query = {value}")

        search_result = self.spotify_client.search_with_query(value, ("track"))
       
        if search_result != None:
            self.result_panel.load_search_result(search_result)
        else:
            self.diary.error("on_input_submitted()", f"Unsuccessful search. Q = {value}")

        #self.result_panel.load_search_result(SearchResult({}))
