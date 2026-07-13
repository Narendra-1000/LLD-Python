from ..enums.rate_limit_type import RateLimitType
from ..limiter.fixed_window_rate_limiter import FixedWindowRateLimiter
from ..limiter.rate_limiter import RateLimiter
from ..limiter.sliding_window_log_rate_limiter import SlidingWindowLogRateLimiter
from ..limiter.token_bucket_rate_limiter import TokenBucketRateLimiter
from ..model.rate_limit_config import RateLimitConfig


class RateLimiterFactory:
    @staticmethod
    def create_rate_limiter(algo: RateLimitType, config: RateLimitConfig) -> RateLimiter:
        if algo == RateLimitType.TOKEN_BUCKET:
            return TokenBucketRateLimiter(config)
        if algo == RateLimitType.FIXED_WINDOW:
            return FixedWindowRateLimiter(config)
        if algo == RateLimitType.SLIDING_WINDOW_LOG:
            return SlidingWindowLogRateLimiter(config)
        raise ValueError(f"Unknown algorithm: {algo}")
