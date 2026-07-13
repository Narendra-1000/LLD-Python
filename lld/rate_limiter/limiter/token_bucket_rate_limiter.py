import threading
import time

from ..enums.rate_limit_type import RateLimitType
from ..model.rate_limit_config import RateLimitConfig
from .rate_limiter import RateLimiter


class TokenBucketRateLimiter(RateLimiter):
    def __init__(self, config: RateLimitConfig) -> None:
        super().__init__(config, RateLimitType.TOKEN_BUCKET)
        self._tokens: dict[str, int] = {}
        self._last_refill_time: dict[str, int] = {}
        self._tokens_lock = threading.Lock()

    def allow_request(self, user_id: str) -> bool:
        allowed = False
        now = int(time.time() * 1000)

        with self._tokens_lock:
            current_tokens = self._refill_tokens(user_id, now)

            if current_tokens > 0:
                allowed = True
                self._tokens[user_id] = current_tokens - 1
            else:
                self._tokens[user_id] = current_tokens

        return allowed

    def _refill_tokens(self, user_id: str, now: int) -> int:
        refill_rate = self.config.window_in_seconds / self.config.max_requests

        last_refill = self._last_refill_time.get(user_id, now)
        elapsed_seconds = (now - last_refill) // 1000
        refill_tokens = int(elapsed_seconds / refill_rate)

        current_tokens = self._tokens.get(user_id, self.config.max_requests)
        current_tokens = min(self.config.max_requests, current_tokens + refill_tokens)
        if refill_tokens > 0:
            self._last_refill_time[user_id] = now

        return current_tokens
