import requests
import urllib.parse
from bs4 import BeautifulSoup
import re
import os
from typing import Union

from .LyricLine import LyricLine
from .Lyric import Lyric


def __get_website_content(website: str) -> str:

    API_TOKEN = os.environ["SCRAPE_API_TOKEN"] 
    

    encoded_url = urllib.parse.quote(website)

    api_url =  f"http://api.scrape.do/?token={API_TOKEN}&url={encoded_url}&render=true"

    response = requests.get(api_url)
    return response.text

def __search_lyricsify_for_song(artist: str, title: str) -> Union[str, None]:
    search_prompt = f"{artist}-{title}"
    url_encoded_search_prompt = urllib.parse.quote(search_prompt)
    request_url = f"https://www.lyricsify.com/search?q={url_encoded_search_prompt}"
    
    html_content = __get_website_content(request_url)

    match_result = re.search(r"\/lyrics?\/[a-zA-Z0-9-\/]+", html_content)
    if match_result == None:
        return None
    return f"https://www.lyricsify.com" + match_result.group()



def __get_timestamp(line: str) -> tuple:
    minute = int(line[1] + line[2])
    second = int(line[4] + line[5])
    m_sec  = int(line[7] + line[8])

    return minute, second, m_sec

def __parse_lines(lines: list[str]) -> Lyric:
   
    lyric = Lyric()

    for indx in range(len(lines) -1):
        current_line = lines[indx]
        next_line    = lines[indx+1]
        
        current_line_timestamp = __get_timestamp(current_line)
        next_line_timestamp = __get_timestamp(next_line)
        formatted_line = LyricLine(current_line[10:],
                                   current_line_timestamp, 
                                   next_line_timestamp)
        lyric.add_line(formatted_line)
    return lyric

def search_for_lyric(artist: str, title: str, uri: str) -> Union[Lyric, None]:
    song_lyrics_url = __search_lyricsify_for_song(title, artist)
    
    if song_lyrics_url == None:
        return None
    
    song_lyrics_website_content = __get_website_content(song_lyrics_url)
    
    if song_lyrics_website_content == None:
        return None


    match_result = re.search("lyrics_[0-9]+_details", song_lyrics_website_content)
    if match_result == None: return None
    html_tag_id = match_result.group()

    soup = BeautifulSoup(song_lyrics_website_content, "html.parser" )
    lyrics_container = soup.find("div", {"id": html_tag_id})
    if lyrics_container == None: return None

    raw_lyrics = lyrics_container.text.split("\n\n")[1]
    
    lyric = __parse_lines(
            raw_lyrics.split("\n")
            )
    
    lyric.uri = uri
    lyric.artists = artist
    lyric.title = title
    
    return lyric

