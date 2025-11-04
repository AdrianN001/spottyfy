from .LyricLine import LyricLine
from typing import Union

class Lyric:
    PARSE_DELIMITER: str = "<>"

    lines : list[LyricLine]

    def __init__(self) -> None:
        self.lines = []


    def add_line(self, line: LyricLine) -> None:
        self.lines.append(line)
    

    def get_line(self, progress_ms: int) -> Union[LyricLine, None]:
        
        for line in self.lines: 
            start_timestamp_ms = line.start[0] * 60_000 + line.start[1]*1000 + line.start[2] * 10
            end_timestamp_ms = line.end[0] * 60_000 + line.end[1]*1000 + line.end[2] *10 
            
            if progress_ms > start_timestamp_ms and progress_ms < end_timestamp_ms:
                return line 
        return None


    def to_parsable_content(self) -> str:
        return "<>".join(x.to_parse_string() for x in self.lines)

    @staticmethod
    def from_parsed_content(parsed_string: str):
        
        lyric = Lyric()
        for line in parsed_string.split("<>"):
            lyric.add_line(
                    LyricLine.load_from_string(line)
                   )


        return lyric
