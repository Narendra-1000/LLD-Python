from ..enums.log_level import LogLevel
from .log_handler import LogHandler


class ErrorHandler(LogHandler):
    def can_handle(self, level: LogLevel) -> bool:
        return level == LogLevel.ERROR
