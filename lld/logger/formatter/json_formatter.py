from datetime import datetime

from ..model.log_message import LogMessage
from .log_formatter import LogFormatter

_FORMATTER = "%Y-%m-%d %H:%M:%S"


class JsonFormatter(LogFormatter):
    def format(self, message: LogMessage) -> str:
        formatted_time = datetime.fromtimestamp(message.timestamp / 1000).strftime(
            _FORMATTER
        )

        return (
            f'{{"timestamp": {formatted_time}, "level": "{message.level.value}", '
            f'"message": "{message.message}"}}'
        )
