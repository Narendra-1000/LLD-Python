from ..formatter.log_formatter import LogFormatter
from ..model.log_message import LogMessage
from .log_appender import LogAppender


class ConsoleAppender(LogAppender):
    def __init__(self, formatter: LogFormatter):
        self._formatter = formatter

    def append(self, message: LogMessage) -> None:
        print(self._formatter.format(message))
