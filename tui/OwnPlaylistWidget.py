

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import ListItem, ListView, Static

from diary.diary import Diary
from spoti.client import SpotifyClient
from tui.PlaylistNameStatic import PlaylistNameStatic
from tui.PlaylistTable import PlaylistTable


class OwnPlaylistWidget(Vertical): 

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)



    def attach_spotify_client(self, spotify_client: SpotifyClient) -> None:
        self.spotify_client = spotify_client


    def attach_diary(self, diary: Diary) -> None:
        self.diary = diary

    def attach_playlist_table(self, playlist_table: PlaylistTable) -> None:
        self.playlist_table = playlist_table

    def compose(self) -> ComposeResult:
        yield ListView(id = "list_view")

    def on_mount(self) -> None:
        self.list_view = self.query_one("#list_view", ListView)
        

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        label = event.item.query_one(PlaylistNameStatic)
        playlist_id = label.playlist_id
        if playlist_id == "saved-tracks": 
            fav_songs = self.spotify_client.fetch_favorite_songs(50)
            self.playlist_table.load_new_songs(fav_songs, context_uri="",isSavedSongs=True)
            return

        playlist = self.spotify_client.fetch_playlist(playlist_id)
        
        self.playlist_table.load_playlist(playlist)



    def load_playlist(self) -> None:
        current_users_playlists = self.spotify_client.fetch_user_playlist()
        
        if current_users_playlists == None: 
            return None
        
        self.list_view.append(ListItem(PlaylistNameStatic("Saved Tracks\n", "saved-tracks")))
        for playlist in current_users_playlists:

            self.list_view.append(
                    ListItem(PlaylistNameStatic(
                        playlist.name,
                        playlist.playlist_id                    
                        ))
                    )

