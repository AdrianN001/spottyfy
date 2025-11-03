from .LyricLine import LyricLine
from typing import Union

class Lyric:
    artists: str
    title:   str
    uri:     str

    lines : list[LyricLine]

    def __init__(self, *, artist: str = "", title: str = "", uri: str = "") -> None:
        self.lines = []


    def add_line(self, line: LyricLine) -> None:
        self.lines.append(line)
    

    def get_line(self, progress_ms: int) -> Union[LyricLine, None]:
        
        for line in self.lines: 
            start_timestamp_ms = line.start[0] * 60_000 + line.start[1]*1000 + line.start[2] * 10
            end_timestamp_ms = line.end[0] * 60_000 + line.end[1]*1000 + line.start[2] *10 
            
            if progress_ms > start_timestamp_ms and progress_ms < end_timestamp_ms:
                return line 
        return None
