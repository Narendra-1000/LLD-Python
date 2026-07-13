import re
from datetime import datetime


class DateTimeParser:
    _PATTERN = re.compile(
        r"^(\d{1,2}) ([A-Za-z]{3}) (\d{1,2}):(\d{2}) (AM|PM) (\d{4})$"
    )

    @staticmethod
    def parse(value: str) -> datetime:
        match = DateTimeParser._PATTERN.match(value)
        if not match:
            raise ValueError(f"Unable to parse datetime: {value}")

        day, month, hour, minute, meridiem, year = match.groups()
        normalized = f"{int(day):02d} {month} {int(hour):02d}:{minute} {meridiem} {year}"
        return datetime.strptime(normalized, "%d %b %I:%M %p %Y")
