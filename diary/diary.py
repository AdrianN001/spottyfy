

from diary.level import Level
from diary.message import Message


class Diary:
    
    messages: list[Message]
    
    def __init__(self) -> None:
        self.messages = []

    def info(self, source: str, content: str) -> None:
        self.__add_to_diary(Level.INFO, source, content)

    def debug(self, source: str, content: str) -> None:
        self.__add_to_diary(Level.DEBUG, source, content)

    def warning(self, source: str, content: str) -> None:
        self.__add_to_diary(Level.WARNING, source, content)

    def error(self, source: str, content: str) -> None:
        self.__add_to_diary(Level.ERROR, source, content)
    
    def clear_diary(self) -> None:
        self.messages.clear()


    def __add_to_diary(self, level: Level, source: str, content: str) -> None:
        self.messages.append(
                Message(level, source, content)
                )
