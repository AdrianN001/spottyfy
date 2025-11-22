from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Static
from textual.timer import Timer

from config.usage import fetch_usage_data_from_scrape
import diary
from diary.diary import Diary
from spoti.client import SpotifyClient
from spoti.profile import Profile
from spoti.usage import SpotifyUsageOverwatch
from tui.DiaryTable import DiaryTable


class DebugStatsWidget(Widget):

    DEFAULT_CSS="""
    #top_container{
        border: yellow;
    }
    #top_left_container{
        width:30%;
    }
    #top_right_container{
        width:  65%;
        height: 100%;
        border: cyan;
    }
    DiaryTable{
        height:100%;
    }
    #spotify_usage_container{
        border: green round;
        height: 40%;
    }
    #spotify_profile_container{
        border: red;
        height: 65%;
    }
    Static{
        color: #bbbbbb;
    }
    #scrape_usage_container{
        border: magenta round;
        height: 30%;
        width: 100%;
    }
    """

    scrape_usage_fetch_timer: Timer
    isActive: bool

    spotify_usage_overwatch: SpotifyUsageOverwatch
    spotify_profile: Profile
    
    diary: Diary

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.isActive = False

    def attach_spoti_usage_manager(self, manager: SpotifyUsageOverwatch) -> None:
        self.spotify_usage_overwatch = manager
    
    def attach_spoti_profile(self, profile: Profile) -> None:
        self.spotify_profile = profile
        self.update_spotify_profile(profile)

    def attach_diary(self, diary: Diary) -> None:
        self.diary = diary

        self.diary_table.attach_diary(self.diary)

    def get_scrape_usage(self) -> None:
        raw_data = fetch_usage_data_from_scrape()
        max_monthly_request = raw_data["MaxMonthlyRequest"]
        remaining_montly_request = raw_data["RemainingMonthlyRequest"]

        new_output = \
                f"[bold #ffffff]Remaining Requests[/bold #ffffff]: {remaining_montly_request}/{max_monthly_request} [red]({int(100-(remaining_montly_request)/(max_monthly_request)*100)}% used)[/red]"
        
        self.scrape_usage_static.update(new_output)
        self.refresh()
    
    def get_spotify_usage(self) -> None:
        if not self.isActive:
            return

        self.spotify_usage_static.update(
                self.spotify_usage_overwatch.__repr__()
                )

    def update_spotify_profile(self, profile: Profile) -> None:
        formatted_text = \
                f"""Logged in as: 
[#ffffff bold]{profile.display_name}[/#ffffff bold] ({profile.email}) from {profile.country}

[#ffffff bold]URI[/#ffffff bold]: {profile.uri}
[#ffffff bold]Subscription Level[/#ffffff bold]: {profile.subscription_level}

[#ffffff bold]Scopes Allowed[/#ffffff bold]: {profile.scope}
                """
        self.spotify_profile_static.update(formatted_text)

    def on_mount(self) -> None:
        self.scrape_usage_static = self.query_one("#scrape_usage", Static)
        self.spotify_usage_static = self.query_one("#spotify_usage", Static)
        self.spotify_profile_static = self.query_one("#spotify_profile_static", Static)

        self.scrape_usage_container = self.query_one("#scrape_usage_container", Widget)
        self.spotify_usage_container = self.query_one("#spotify_usage_container", Widget)
        self.spotify_profile_container = self.query_one("#spotify_profile_container", Widget)

        self.scrape_usage_container.border_title = "|> Scrape.do statistics <|"
        self.spotify_usage_container.border_title = "|> Spotify API usage statistics <|"
        self.spotify_profile_container.border_title ="|> Spotify Profile <|"

        self.diary_table = self.query_one("#diary_table", DiaryTable)
        

        self.scrape_usage_fetch_timer = self.set_interval(90, self.get_scrape_usage)
        self.spotify_usage_fetch_timer = self.set_interval(1, self.get_spotify_usage)

    def compose(self) -> ComposeResult:

        yield Horizontal(
                Vertical(
                    Widget(
                        Static("Fetching", id="scrape_usage")
                    , id="scrape_usage_container"),
                    Widget(
                        Static(id="spotify_profile_static"),
                        id="spotify_profile_container"
                        ),
                    id="top_left_container"
                ),
                Vertical(
                    Widget(
                        Static("Fetching", id="spotify_usage")
                    , id="spotify_usage_container"),
                    DiaryTable(
                        id="diary_table"
                        ),
                    id = "top_right_container"
                ),
             id="top_container")
