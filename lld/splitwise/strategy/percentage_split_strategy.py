from typing import Dict, List

from ..model.split import Split
from ..model.user import User
from .split_strategy import SplitStrategy


class PercentageSplitStrategy(SplitStrategy):
    def split(
        self,
        total_amount: float,
        participants: List[User],
        metadata: Dict[User, float],
    ) -> List[Split]:
        total_percent = sum(metadata.values())
        if total_percent != 100.0:
            raise ValueError("Total percent should be 100")

        splits: List[Split] = []
        for user in participants:
            splits.append(
                Split(user, total_amount * metadata.get(user, 0.0) / 100)
            )
        return splits
