import threading
import time

from ..enums.rate_limit_type import RateLimitType
from ..model.rate_limit_config import RateLimitConfig
from .rate_limiter import RateLimiter


class FixedWindowRateLimiter(RateLimiter):
    def __init__(self, config: RateLimitConfig) -> None:
        super().__init__(config, RateLimitType.FIXED_WINDOW)
        self._request_count: dict[str, int] = {}
        self._window_start: dict[str, int] = {}
        self._request_count_lock = threading.Lock()

    def allow_request(self, user_id: str) -> bool:
        allowed = False
        current_req_window = int(time.time()) // self.config.window_in_seconds

        with self._request_count_lock:
            last_req_window = self._window_start.get(user_id, current_req_window)

            if last_req_window != current_req_window:
                self._window_start[user_id] = current_req_window
                allowed = True
                self._request_count[user_id] = 1
            else:
                count = self._request_count.get(user_id, 0)
                if count < self.config.max_requests:
                    allowed = True
                    self._request_count[user_id] = count + 1
                else:
                    self._request_count[user_id] = count

        return allowed
