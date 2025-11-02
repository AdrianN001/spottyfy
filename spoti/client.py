import spotipy
from spotipy.oauth2 import SpotifyOAuth

from spoti.song import Song
from spoti.playback_song import PlaybackSong
from spoti.playlist_song import PlayListSong

from typing import Union

class SpotifyClient:
    sp:             spotipy.Spotify
    current_song:   PlaybackSong


    def __init__(self, client_id: str, client_secret: str):
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret= client_secret, 
            redirect_uri="http://127.0.0.1:8080/",
            scope="user-modify-playback-state user-library-read user-read-playback-state"
        ))

    

    # Operations

    # Fetches the current song
    def fetch_current_song(self) -> Union[PlaybackSong, None]:
        raw_playback = self.sp.current_playback()

        if not raw_playback or not raw_playback["is_playing"]:
            return None
        
        progress_ms = raw_playback["progress_ms"]
        duration_ms = raw_playback["item"]["duration_ms"]
        song_name = raw_playback["item"]["name"]

        progress_sec, duration_sec = progress_ms / 1000, duration_ms / 1000
        
        self.current_song = PlaybackSong(
                song_name, 
                [artist['name'] for artist in raw_playback['item']['artists']],
                raw_playback['item']['album']['name'],
                duration_sec,
                raw_playback['item']['uri'],
                progress_sec
                )
        
        return self.current_song

    def fetch_favorite_songs(self, max_fetch: int) -> Union[list[PlayListSong], None]: 
        limit = 50
        offset = 0 
        
        liked_songs: list[PlayListSong] = []

        while offset < max_fetch: 
            results = self.sp.current_user_saved_tracks(limit, offset)
            if not results:
                break

            items = results['items']
            
            for item in items: 
                added_at = item['added_at']
                track = item['track']
                
                liked_songs.append(
                        PlayListSong(
                            track['name'],
                            [x['name'] for x in track['artists']],
                            track['album']['name'],
                            track['duration_ms'] / 1000,
                            track['uri'],
                            added_at
                            )
                        )       

            offset += limit

        return liked_songs

    def play_song_from_saved(self, position: int) -> None:
        self.sp.start_playback(context_uri="spotify:collection", offset={"position": position})
    
    def play_song_from_playlist(self, context_uri: str, uri: str) -> None:
        self.sp.start_playback(context_uri=context_uri, offset={"uri": uri})
