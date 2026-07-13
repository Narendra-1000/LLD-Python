from ..enums.split_type import SplitType
from ..strategy.equal_split_strategy import EqualSplitStrategy
from ..strategy.percentage_split_strategy import PercentageSplitStrategy
from ..strategy.split_strategy import SplitStrategy


class SplitStrategyFactory:
    @staticmethod
    def get_strategy(split_type: SplitType) -> SplitStrategy:
        if split_type == SplitType.EQUAL:
            return EqualSplitStrategy()
        if split_type == SplitType.PERCENTAGE:
            return PercentageSplitStrategy()
        raise ValueError(f"Unsupported split type: {split_type}")
