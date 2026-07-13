import time

from .enums.log_level import LogLevel
from .log_handler_configuration import LogHandlerConfiguration
from .model.log_message import LogMessage


class Logger:
    _instance: "Logger | None" = None

    def __init__(self):
        self._handler_chain = LogHandlerConfiguration.build()

    @classmethod
    def get_instance(cls) -> "Logger":
        if cls._instance is None:
            cls._instance = Logger()
        return cls._instance

    def log(self, level: LogLevel, message: str) -> None:
        msg = LogMessage(level, message, int(time.time() * 1000))
        self._handler_chain.handle(msg)

    def debug(self, msg: str) -> None:
        self.log(LogLevel.DEBUG, msg)

    def info(self, msg: str) -> None:
        self.log(LogLevel.INFO, msg)

    def warn(self, msg: str) -> None:
        self.log(LogLevel.WARN, msg)

    def error(self, msg: str) -> None:
        self.log(LogLevel.ERROR, msg)

    def fatal(self, msg: str) -> None:
        self.log(LogLevel.FATAL, msg)
