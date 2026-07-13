from dataclasses import dataclass

from .user import User


@dataclass
class Split:
    user: User
    amount: float

    def __str__(self) -> str:
        return f"Split(user={self.user}, amount={self.amount})"
