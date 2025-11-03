

class LyricLine:

    content: str

    start:   tuple[int, int, int]
    end  :   tuple[int, int, int]

    def __init__(self, content: str, start: tuple, end: tuple) -> None:
        self.content = content
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"
