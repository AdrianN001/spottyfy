

from textual.widgets import Static


class LyricContainer(Static):
    
    def update_content(self, content: str) -> None:
        self.update(content)
