

from diary.level import Level


class Message:

    level: Level

    source: str 
    content: str

    def __init__(self, level: Level, source: str, content: str) -> None:
        self.level = level
        self.source = source
        self.content = content
