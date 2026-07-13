from abc import ABC, abstractmethod
from typing import Dict, List

from ..model.split import Split
from ..model.user import User


class SplitStrategy(ABC):
    @abstractmethod
    def split(
        self,
        total_amount: float,
        participants: List[User],
        metadata: Dict[User, float],
    ) -> List[Split]:
        pass
