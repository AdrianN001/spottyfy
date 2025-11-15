import inspect

class SpotifyUsageOverwatch:

    call_frequency: dict
    def __init__(self) -> None:
        self.call_frequency = {}


    def add_to_usage(self):
        caller_funtion = inspect.stack()[1].function
        caller_funtion += "()"

        if caller_funtion in self.call_frequency:
            self.call_frequency[caller_funtion] += 1
        else:
            self.call_frequency[caller_funtion] = 1


    def __repr__(self) -> str:
        return f"{self.call_frequency}"
