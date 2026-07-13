from dataclasses import dataclass
from typing import List

from ..enums.split_type import SplitType
from .split import Split
from .user import User


@dataclass
class Expense:
    description: str
    amount: float
    paid_by: User
    splits: List[Split]
    split_type: SplitType

    def __str__(self) -> str:
        return (
            f"Expense(description={self.description!r}, amount={self.amount}, "
            f"paid_by={self.paid_by}, splits={self.splits}, "
            f"split_type={self.split_type})"
        )
