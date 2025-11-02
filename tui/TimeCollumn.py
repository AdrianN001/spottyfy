

from rich.progress import ProgressColumn
from rich.text import Text

class TimeCollumn(ProgressColumn):

    def render(self, task):
        completed = int(task.completed)
        total = int(task.total)

        return Text(f"{completed//60}:{completed%60:02d} / {total//60}:{total%60:02d}", style="bold green")
