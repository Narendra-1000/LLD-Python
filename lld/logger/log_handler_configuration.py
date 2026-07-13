from .appenders.log_appender import LogAppender
from .enums.log_level import LogLevel
from .handlers.debug_handler import DebugHandler
from .handlers.error_handler import ErrorHandler
from .handlers.fatal_handler import FatalHandler
from .handlers.info_handler import InfoHandler
from .handlers.log_handler import LogHandler
from .handlers.warn_handler import WarnHandler


class LogHandlerConfiguration:
    _debug = DebugHandler()
    _info = InfoHandler()
    _warn = WarnHandler()
    _error = ErrorHandler()
    _fatal = FatalHandler()

    @classmethod
    def build(cls) -> LogHandler:
        cls._debug.next = cls._info
        cls._info.next = cls._warn
        cls._warn.next = cls._error
        cls._error.next = cls._fatal

        return cls._debug

    @classmethod
    def add_appender_for_level(cls, level: LogLevel, appender: LogAppender) -> None:
        if level == LogLevel.DEBUG:
            cls._debug.subscribe(appender)
        elif level == LogLevel.INFO:
            cls._info.subscribe(appender)
        elif level == LogLevel.WARN:
            cls._warn.subscribe(appender)
        elif level == LogLevel.ERROR:
            cls._error.subscribe(appender)
        elif level == LogLevel.FATAL:
            cls._fatal.subscribe(appender)
