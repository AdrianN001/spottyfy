from functools import lru_cache
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from diary.diary import Diary
from lyrics.Lyric import Lyric
from spoti.Playlist import Playlist
from spoti.SearchResult import SearchResult
from spoti.artist import Artist
from spoti.profile import Profile
from spoti.song import Song
from spoti.playback_song import PlaybackSong
from spoti.playlist_song import PlayListSong
from spoti.usage import SpotifyUsageOverwatch

from typing import Iterable, Union

class SpotifyClient:
    SCOPE="user-modify-playback-state user-read-private user-library-read user-read-playback-state user-read-email playlist-read-private"

    sp:             spotipy.Spotify
    current_song:   PlaybackSong
    current_lyric:  Union[Lyric, None]
    usage_manager:  SpotifyUsageOverwatch
    diary:          Diary


    def __init__(self, client_id: str, client_secret: str):
        self.current_lyric = None 
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret= client_secret, 
            redirect_uri="http://127.0.0.1:8080/",
            scope=SpotifyClient.SCOPE
            ))

        self.usage_manager = SpotifyUsageOverwatch()

        # Temporary, it'll be synced by attach_diary()
        self.diary = Diary()

    
    def attach_diary(self, diary: Diary) -> None:
        for message in self.diary.messages:
            diary.messages.append(message)

        self.diary = diary

    # Operations

    # Fetches the current song
    def fetch_current_song(self) -> Union[PlaybackSong, None]:
        raw_playback = self.sp.current_playback()
        self.usage_manager.add_to_usage()

        if not raw_playback:
            return self.diary.error("fetch_current_song()", "Tried to fetch current song, but was not able.")

        if not raw_playback["item"]:
            return self.diary.error("fetch_current_song()", "Tried to fetch current song, but was not able.")

        progress_ms = raw_playback["progress_ms"]
        duration_ms = raw_playback["item"]["duration_ms"]
        song_name = raw_playback["item"]["name"]

        progress_sec, duration_sec = progress_ms / 1000, duration_ms / 1000
        

        self.current_song = PlaybackSong(
                song_name, 
                [Artist(artist) for artist in raw_playback['item']['artists']],
                raw_playback['item']['album']['name'],
                duration_sec,
                raw_playback['item']['uri'],
                progress_sec,
                raw_playback["is_playing"],
                progress_ms,
                raw_playback['item']["album"]["images"][2]["url"]
                )
        
        #self.diary.info("fetch_current_song()", "Successfully fetched the actuall song.")
        return self.current_song

    def fetch_user_profile(self) -> Profile:
        me_raw = self.sp.current_user()
        self.usage_manager.add_to_usage()
        
        assert me_raw != None

        me = Profile(me_raw, SpotifyClient.SCOPE)
        self.diary.info("fetch_user_profile", "Successfully fetched current user's profile.")
        return me

    def fetch_favorite_songs(self, max_fetch: int) -> Union[list[PlayListSong], None]: 
        limit = 50
        offset = 0 
        
        liked_songs: list[PlayListSong] = []

        while offset < max_fetch: 
            results = self.sp.current_user_saved_tracks(limit, offset)
            self.usage_manager.add_to_usage()
            if not results:
                break

            items = results['items']
            
            for item in items: 
                added_at = item['added_at']
                track = item['track']
                
                liked_songs.append(
                        PlayListSong(
                            track['name'],
                            [Artist(x) for x in track['artists']],
                            track['album']['name'],
                            track['duration_ms'] / 1000,
                            track['uri'],
                            added_at
                            )
                        )       

            offset += limit

        self.diary.info("fetch_favorite_songs()", "Successfully fetched the saved songs.")
        return liked_songs

    def fetch_playlist(self, playlist_id: str) -> Union[Playlist, None]:
        raw_response = self.sp.playlist(playlist_id)
        self.usage_manager.add_to_usage()
        if raw_response == None:
            self.diary.warning("fetch_playlist()", "Unsuccessful playlist fetch")
            return None
        self.diary.info("fetch_playlist()", "Successfully fetched a playlist.")

        playlist = Playlist(raw_response)
        return playlist


    def fetch_user_playlist(self) -> Union[list[Playlist], None]: 
        raw_response = self.sp.current_user_playlists()
        self.usage_manager.add_to_usage()

        if raw_response == None:
            self.diary.error("fetch_user_playlist()", "Unsuccessful playlist fetch")
            return None
        self.diary.info("fetch_user_playlist()", "Successfully fetched the playlists of the user.")
        
        return [Playlist(raw_playlist) for raw_playlist in raw_response["items"]]

    def play_song_from_saved(self, position: int) -> None:
        self.sp.start_playback(context_uri="spotify:collection", offset={"position": position})
        self.usage_manager.add_to_usage()
        self.diary.info("play_song_from_saved()", f"New saved song was played, with position: {position}")

    def play_song_from_playlist(self, context_uri: str, uri: str) -> None:
        self.sp.start_playback(context_uri=context_uri, offset={"uri": uri})
        self.usage_manager.add_to_usage()
        self.diary.info("play_song_from_playlist()", "New song was played, with URI: {uri}")


    def jump_forward(self, seconds: int) -> None:
        self.usage_manager.add_to_usage()
        
        progress_second = self.current_song.progress_sec
        duration_second = self.current_song.duration_sec

        seeked_ms = (progress_second + seconds) * 1000
        seeked_ms = min(seeked_ms, (duration_second*1000) )
       
        seeked_ms = int(seeked_ms)
        self.diary.info("jump_forward()", f"{progress_second=} {seeked_ms=}")

        try:
            self.sp.seek_track(seeked_ms)
        except:
            self.diary.error("jump_forward()", "Couldnt skip forward.")
    
    def jump_backward(self, seconds: int) -> None:
        self.usage_manager.add_to_usage()
        
        progress_second = self.current_song.progress_sec

        seeked_ms = (progress_second - seconds) * 1000
        seeked_ms = max(seeked_ms, 0)

        seeked_ms = int(seeked_ms)
        try:
            self.sp.seek_track(position_ms=seeked_ms)
        except:
            self.diary.error("jump_backward()", "Couldnt jump back.")
    


    def get_next_song(self):
        data = self.sp._get("me/player/queue")
        self.usage_manager.add_to_usage()
        

        if not data or not data["queue"]:
            self.diary.error("get_next_song()", "Tried to fetch the next song in the queue, but was not able.")
            return None
        raw_song = data["queue"][0]  # nächster Song
        
        self.diary.info("get_next_song()", "Successfully fetched the next song in the queue.")
        return Song(
            raw_song["name"],
            [Artist(x) for x in raw_song["artists"]],
            raw_song["album"]['name'],
            raw_song["duration_ms"] / 1000,
            raw_song['uri']
                )

    @lru_cache()
    def search_with_query(self, q: str, type_of_search: Iterable[str]) -> Union[SearchResult, None]:
        raw_search_result = self.sp.search(
                q, 
                limit=20,
                type = "track,playlist"
                )
        self.diary.info("search_with_query()", "Search ended in spotify client.")
        self.usage_manager.add_to_usage()

        if raw_search_result == None: 
            return None
        
        formatted_search_result = SearchResult(q, raw_search_result)
        
        return formatted_search_result

    # lyrics
    
    def set_current_lyrics(self, lyric: Lyric) -> None:
        self.current_lyric = lyric

    # Musik Operations

    # Skips the song
    def skip(self) -> None:
        self.sp.next_track()
        self.usage_manager.add_to_usage()
        self.diary.info("skip()", "Actual music was skipped.")

    # Skips to the previous song
    def prev(self) -> None:
        self.sp.previous_track()
        self.usage_manager.add_to_usage()
        self.diary.info("prev()", "Music was changed to the previous song.")

    # Stops/Starts the song
    def toggle_playback(self) -> None:
        if self.current_song.isPlaying:
            self.sp.pause_playback()
            self.diary.info("toggle_playback()", "Music paused.")
        else:
            self.sp.start_playback()
            self.diary.info("toggle_playback()", "Music started.")

        self.usage_manager.add_to_usage()

    
    def start_song(self, song_uri: str) -> None:
        self.sp.start_playback(uris=[song_uri])
        self.usage_manager.add_to_usage()
