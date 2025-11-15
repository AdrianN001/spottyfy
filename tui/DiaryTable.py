


from textual import messages
from textual.timer import Timer
from textual.widgets import DataTable

from diary.diary import Diary


class DiaryTable(DataTable):

    diary:              Diary

    diary_update_timer: Timer

    diary_index:        int

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setup_columns()
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.fixed_rows = 0
        self.show_header = True
        self.diary_index = 1
    
    def attach_diary(self, diary: Diary) -> None:
        self.diary = diary

    def setup_columns(self) -> None:
        self.clear(columns=True)

        self.add_columns(
                "#",
                "LEVEL",
                "SOURCE",
                "CONTENT"
                )

    def on_mount(self):
        super().on_mount()

        self.diary_update_timer = self.set_interval(1, self.update_ui)


    def update_ui(self) -> None:
        if not hasattr(self, "diary"): return
        if len(self.diary.messages) == 0: return

    
        for message in self.diary.messages:
            self.add_row(
                        str(self.diary_index),
                        message.level.name,
                        message.source,
                        message.content
                    )
            self.diary_index += 1

        self.refresh()
        self.diary.clear_diary() 
