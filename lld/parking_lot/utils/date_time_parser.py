from datetime import datetime


class DateTimeParser:
    @staticmethod
    def parse(input_str: str) -> datetime:
        return datetime.strptime(input_str, "%d %b %I:%M %p %Y")
