import textwrap
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Markdown
from spoti.playback_song import PlaybackSong
from spoti.song import Song
from tui.ImageWidget import ImageWidget
from typing import Union

class CurrentSongView(Vertical):
    DEFAULT_CSS = """
    CurrentSongView{
        border: round cyan;
    }

    #top-section {
        height: 50%;
        padding: 1;
        background: #101010;
        border: round #1DB954;
        /* border: yellow round; */
    }

    #artist-image {
        width: 60%;
        height: 90%;
        /* border: round #1DB954; */
    }

    #info-box {
        padding-top: 5;
        padding-left: 2;
    }

    #song-title {
        color: #1DB954;
        text-style: bold;
        margin-bottom: 1;
    }

    #artist-name {
        color: #cccccc;
        margin-bottom: 1;
    }

    #artist-description {
        padding: 1;
        width: 100%;
        height: 40%;
        margin-top: 0;
        background: #0f0f0f;
        color: #dddddd;
    }
    

    #next_song {
        margin-top: 1;
        width: 100%;
    }
    """

    current_song: Union[PlaybackSong, None]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_song = None

    def update_current_song(self, new_current_song: PlaybackSong) -> None:
        self.current_song = new_current_song
        self.query_one("#song-title", Label).update(new_current_song.title)
        self.query_one("#artist-name", Label).update(", ".join(x.name for x in new_current_song.artists[:2]))

        artist_image_widget = self.query_one("#artist-image", ImageWidget)
        artist_image_widget.load_image(new_current_song.album_image_url)
        artist_image_widget.refresh()

        self.update_description(new_current_song.title, [x.name for x in new_current_song.artists[:2]])

    def update_description(self, title: str, artists: list[str]) -> None:

        text = f"""
                # {', '.join(artists)}
                ------------------------
                Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,
                """

        text = textwrap.dedent(text)

        markdown_viewer = self.query_one("#artist-description", Markdown)


        markdown_viewer.update(text)

    def update_next_song(self, next_song: Song) -> None:
        container = self.query_one("#next_song", Label)
        start_space_width = space_width = int(self.size.width * 0.95)
        space_width -= len("Next --> ")
        
        need_new_line = False
       
        song_text = f"{next_song.title} from: {','.join( x.name for x in next_song.artists[:2])}"
        space_width -= len(song_text)
        if space_width < 0:
            need_new_line = True
            space_width = start_space_width - len(song_text)

        song_text_formatted = f"[magenta]'{next_song.title}'[/magenta] from: [green]{','.join( x.name for x in next_song.artists[:2])}[/green]"

        if need_new_line:
            container.styles.margin = (3,0,0,0)
            song_text_formatted = "\n" + song_text_formatted
        else:
            container.styles.margin = (4,0,0,0)

        container.update(f"Next --> {' '*space_width} {song_text_formatted}")



    def compose(self) -> ComposeResult:
        yield Horizontal(
            ImageWidget(id="artist-image"),
            Vertical(
                Label("Title", id="song-title"),
                Label("Artist", id="artist-name"),
                id="info-box"
            ),
            id="top-section"
        )
        yield Markdown("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. ", id="artist-description")
        yield Label("", id="next_song")

