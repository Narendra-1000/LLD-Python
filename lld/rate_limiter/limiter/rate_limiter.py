from abc import ABC, abstractmethod

from ..enums.rate_limit_type import RateLimitType
from ..model.rate_limit_config import RateLimitConfig


class RateLimiter(ABC):
    def __init__(self, config: RateLimitConfig, type_: RateLimitType) -> None:
        self.config = config
        self.type = type_

    @abstractmethod
    def allow_request(self, user_id: str) -> bool:
        pass
