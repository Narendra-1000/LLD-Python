import threading
import traceback

from ..formatter.log_formatter import LogFormatter
from ..model.log_message import LogMessage
from .log_appender import LogAppender


class FileAppender(LogAppender):
    def __init__(self, formatter: LogFormatter, file_name: str):
        self._formatter = formatter
        self._lock = threading.Lock()
        try:
            self._file = open(file_name, "a", encoding="utf-8")
        except OSError as e:
            raise RuntimeError("Failed to open log file") from e

    # t1, t2, t3,
    def append(self, message: LogMessage) -> None:
        # t4, t5

        # blocking queue -> worker threads
        with self._lock:
            try:
                self._file.write(self._formatter.format(message))
                self._file.write("\n")
                self._file.flush()  # flush can be batched or delayed
            except OSError:
                traceback.print_exc()

    # t1 t2 t3

    # blocking queue of cap = 3
    # 3 worker threads

    def close(self) -> None:
        with self._lock:
            try:
                self._file.close()
            except OSError:
                traceback.print_exc()
