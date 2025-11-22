from spoti import PlaybackSong
from typing import Union

from textual.widgets import Static
from textual.reactive import reactive

from spoti.playlist_song import PlayListSong


class PlaybackBar(Static):
    
    completed_seconds = reactive(0)
    isActive = reactive(True)
    duration = 0                # Sekunden (z. B. 3 Minuten)

    title: str
    artists: str

    def set_new_song(self, new_song: PlaybackSong) -> None:
        self.duration = new_song.duration_sec
        self.title = new_song.title
        self.artists = ",".join(x.name for x in new_song.artists[:2])

    def render(self) -> str:
        """Zeichnet den Fortschrittsbalken"""
        
        if (self.duration == 0): return "Kein Song"

        

        TIME_LENGTH = 12
        START_LENGTH = len(self.title) + len(self.artists) + 1

        progress = self.completed_seconds / self.duration
        
        width = self.size.width - TIME_LENGTH - 6 - START_LENGTH  # Platz für Zeit
        filled = int(width * progress)
        bar = f"[magenta]{'─'*filled}[/magenta]" if self.isActive else f"[red]{'─'*filled}[/red]"  
        bar += "[grey]─[/grey]"
        bar += f"{'─'*(width-filled)}"

        minutes, seconds = divmod(int(self.completed_seconds), 60)
        total_min, total_sec = divmod(int(self.duration), 60)
        time_text = f"{minutes:02}:{seconds:02} / {total_min:02}:{total_sec:02}"

        return f"[cyan]{self.title}[/cyan]-{self.artists} {bar} [#00ff00 ]{time_text}[/#00ff00 ]"



