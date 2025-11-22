


from rich.text import Text
from textual.widgets import Static


class PlaylistNameStatic(Static):
    
    playlist_id:    str
    playlist_name:  str
    
    def __init__(self, playlist_name: str, playlist_id: str, *args, **kwargs) -> None: 
        super().__init__(*args, **kwargs)
        self.playlist_name = playlist_name
        self.playlist_id = playlist_id
        

    def render(self) -> Text:
        return Text(self.playlist_name)
