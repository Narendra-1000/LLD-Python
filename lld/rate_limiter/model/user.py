from dataclasses import dataclass

from ..enums.user_tier import UserTier


@dataclass
class User:
    user_id: str
    tier: UserTier
