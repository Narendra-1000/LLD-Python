from datetime import time


def convert_string_to_local_time(value: str) -> time:
    parts = value.split(":")
    return time(hour=int(parts[0]), minute=int(parts[1]))
