
from asyncio import Event
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.events import Enter
from textual.widgets import Input

from diary.diary import Diary
from spoti.SearchResult import SearchResult
from spoti.client import SpotifyClient
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
    

    def on_input_submitted(self, event: Input.Submitted) -> None:
        value = event.input.value
        event.input.value = ""
        self.diary.info("on_input_submitted()", f"Search started: Query = {value}")

        search_result = self.spotify_client.search_with_query(value, ("track"))
       
        if search_result != None:
            self.result_panel.load_search_result(search_result)
        else:
            self.diary.error("on_input_submitted()", f"Unsuccessful search. Q = {value}")

        #self.result_panel.load_search_result(SearchResult({}))
