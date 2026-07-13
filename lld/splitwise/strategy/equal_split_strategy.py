from typing import Dict, List

from ..model.split import Split
from ..model.user import User
from .split_strategy import SplitStrategy


class EqualSplitStrategy(SplitStrategy):
    def split(
        self,
        total_amount: float,
        participants: List[User],
        metadata: Dict[User, float],
    ) -> List[Split]:
        share = total_amount / len(participants)
        splits: List[Split] = []
        for user in participants:
            splits.append(Split(user, share))
        return splits
