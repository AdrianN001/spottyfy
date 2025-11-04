
def get_timestamp_from_line(line: str) -> tuple[int, int, int]:
    minute = int(line[1] + line[2])
    second = int(line[4] + line[5])
    m_sec  = int(line[7] + line[8])

    return minute, second, m_sec



class LyricLine:

    content: str

    start:   tuple[int, int, int]
    end  :   tuple[int, int, int]

    def __init__(self, content: str, start: tuple[int, int, int], end: tuple[int, int, int]) -> None:
        self.content = content
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


    @staticmethod
    def load_from_string(parsed_line: str):
        timestamp_length = len("[00:00.00]")
        start_unparsed = parsed_line[: timestamp_length]
        end_unparsed = parsed_line[-timestamp_length: ]

        start = get_timestamp_from_line(start_unparsed)
        end   = get_timestamp_from_line(end_unparsed)

        content = parsed_line[timestamp_length: -timestamp_length]


        return LyricLine(content, start, end)


    def to_parse_string(self) -> str:
        ret_string = f"[{self.start[0]:02d}:{self.start[1]:02d}.{self.start[2]:02d}]"
        ret_string += self.content
        ret_string += f"[{self.end[0]:02d}:{self.end[1]:02d}.{self.end[2]:02d}]"
        return ret_string
