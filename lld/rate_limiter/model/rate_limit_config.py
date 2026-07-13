from dataclasses import dataclass


@dataclass
class RateLimitConfig:
    max_requests: int
    window_in_seconds: int
