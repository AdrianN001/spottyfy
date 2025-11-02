

def convert_sec_to_min_sec(sec: int) -> tuple[int, int]:
    minutes = int(sec / 60)
    seconds = int(sec % 60)

    return minutes,seconds
