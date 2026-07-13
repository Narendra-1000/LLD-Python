from abc import ABC, abstractmethod

from ..appenders.log_appender import LogAppender
from ..enums.log_level import LogLevel
from ..model.log_message import LogMessage


class LogHandler(ABC):
    def __init__(self):
        self.next: LogHandler | None = None
        self._appenders: list[LogAppender] = []

    def subscribe(self, observer: LogAppender) -> None:
        self._appenders.append(observer)

    def notify_observers(self, message: LogMessage) -> None:
        for appender in self._appenders:
            appender.append(message)

    def handle(self, message: LogMessage) -> None:
        if self.can_handle(message.level):
            self.notify_observers(message)
        elif self.next is not None:
            self.next.handle(message)

    @abstractmethod
    def can_handle(self, level: LogLevel) -> bool:
        pass


# [console, file]

# removes the file
