from abc import ABC, abstractmethod

from ..model.log_message import LogMessage


class LogFormatter(ABC):
    @abstractmethod
    def format(self, message: LogMessage) -> str:
        pass
