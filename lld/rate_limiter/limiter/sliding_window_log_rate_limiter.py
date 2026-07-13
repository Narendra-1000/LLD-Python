import threading
import time
from collections import deque

from ..enums.rate_limit_type import RateLimitType
from ..model.rate_limit_config import RateLimitConfig
from .rate_limiter import RateLimiter


class SlidingWindowLogRateLimiter(RateLimiter):
    def __init__(self, config: RateLimitConfig) -> None:
        super().__init__(config, RateLimitType.SLIDING_WINDOW_LOG)
        self._request_log: dict[str, deque[int]] = {}
        self._request_log_lock = threading.Lock()

    def allow_request(self, user_id: str) -> bool:
        allowed = False
        now = int(time.time())

        with self._request_log_lock:
            log = self._request_log.get(user_id)
            if log is None:
                log = deque()

            while log and (now - log[0]) >= self.config.window_in_seconds:
                log.popleft()

            if len(log) < self.config.max_requests:
                log.append(now)
                allowed = True

            self._request_log[user_id] = log

        return allowed
