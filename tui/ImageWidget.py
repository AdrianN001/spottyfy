from textual.widget import Widget
from rich_pixels import Pixels
from rich.console import RenderResult
import requests
from PIL import Image
from io import BytesIO

from textual.widgets import Static

class ImageWidget(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pixels = None

    def load_image(self, image_url: str) -> None:
        resp = requests.get(image_url)
        img = Image.open(BytesIO(resp.content))
        img.thumbnail((int(33*(16/9)), 30), Image.Resampling.LANCZOS)
        self.pixels = Pixels.from_image(img)

    def render(self) -> RenderResult:
        if self.pixels == None:
            return ""
        return self.pixels


