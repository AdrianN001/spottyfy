
from asyncio import Event
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.events import Enter
from textual.widgets import Input

from diary.diary import Diary


class SearchBar(Input):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.cursor_blink = False
        self.valid_empty = False
        self.placeholder="Search..."


    def attach_diary(self, diary: Diary) -> None:
        self.diary = diary


    def on_input_submitted(self, event: Input.Submitted) -> None:
        value = event.input.value
        event.input.value = ""
        self.diary.info("on_input_submitted()", value)
