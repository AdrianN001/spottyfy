

from typing import Union


class InputQueue:

    queue: list

    interval: float

    initial_interval: float
    frame_time: float

    def __init__(self, interval: float, frame_time: float) -> None:
        self.queue = []
        self.initial_interval = self.interval = interval
        self.frame_time = frame_time


    def tick(self) -> Union[int, None]:
        if len(self.queue) == 0: return None
        self.interval -= self.frame_time

        
        if self.interval <= 0:
            inputs_added = self.acc_queue_and_clear()
            self.interval = self.initial_interval

            if inputs_added == 0:
                return None
            return inputs_added 
        return None

    def add_input(self, value: int) -> None:
        self.queue.append(value)

    def acc_queue_and_clear(self) -> int: 
        sum_of_values = sum(self.queue)
        self.queue.clear()
        return sum_of_values
