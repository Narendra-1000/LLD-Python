from abc import ABC, abstractmethod

from ..model.log_message import LogMessage


class LogAppender(ABC):
    @abstractmethod
    def append(self, message: LogMessage) -> None:
        pass
