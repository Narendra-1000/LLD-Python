from dataclasses import dataclass

from ..enums.log_level import LogLevel


@dataclass
class LogMessage:
    level: LogLevel
    message: str
    timestamp: int
