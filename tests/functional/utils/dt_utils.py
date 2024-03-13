from time import time


def get_milliseconds_timestamp() -> int:
    return int(time() * 1000)
