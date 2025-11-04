import os
from pathlib import Path
from .constants import *

def generate_config_directory() -> None:
    
    dirs_to_create = [
            HOME + CONFIG_DIRECTORY + CUSTOM_DIRECTORY,
            HOME + CONFIG_DIRECTORY + CUSTOM_DIRECTORY + LYRIC_CACHE_DIR,
            HOME + CONFIG_DIRECTORY + CUSTOM_DIRECTORY + PlAYLIST_CACHE_DIR
            ]
    
    for directory in dirs_to_create:
        try:
            os.mkdir(directory)
        except FileExistsError:
            print(directory + " exists")
