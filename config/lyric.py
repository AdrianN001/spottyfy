from typing import Union
import os
from .constants import *

def lyric_cahce_file_exists(uri: str) -> bool:
    return os.path.isfile(
            HOME+CONFIG_DIRECTORY+CUSTOM_DIRECTORY+LYRIC_CACHE_DIR+f"{uri}.txt"
            )

def open_lyric_cache_file(uri: str) -> Union[str, None]:
    
    with open(
            HOME+CONFIG_DIRECTORY+CUSTOM_DIRECTORY+LYRIC_CACHE_DIR+f"{uri}.txt",
            "r",
            ) as file:
        
        return file.read()

def write_lyric_cache_file(raw_content: str, uri: str) -> None:
    
    with open(
            HOME+CONFIG_DIRECTORY+CUSTOM_DIRECTORY+LYRIC_CACHE_DIR+f"{uri}.txt",
            "w",
            ) as file:
        
        file.write(raw_content)


