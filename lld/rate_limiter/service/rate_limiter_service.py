from ..enums.rate_limit_type import RateLimitType
from ..enums.user_tier import UserTier
from ..factory.rate_limiter_factory import RateLimiterFactory
from ..limiter.rate_limiter import RateLimiter
from ..model.rate_limit_config import RateLimitConfig
from ..model.user import User


class RateLimiterService:
    def __init__(self) -> None:
        self._rate_limiters: dict[UserTier, RateLimiter] = {
            UserTier.FREE: RateLimiterFactory.create_rate_limiter(
                RateLimitType.TOKEN_BUCKET,
                RateLimitConfig(max_requests=10, window_in_seconds=60),
            ),
            UserTier.PREMIUM: RateLimiterFactory.create_rate_limiter(
                RateLimitType.FIXED_WINDOW,
                RateLimitConfig(max_requests=100, window_in_seconds=60),
            ),
        }

    def allow_request(self, user: User) -> bool:
        limiter = self._rate_limiters.get(user.tier)
        if limiter is None:
            raise ValueError(f"No limiter configured for tier: {user.tier}")
        return limiter.allow_request(user.user_id)
