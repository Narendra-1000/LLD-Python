from abc import ABC, abstractmethod
from typing import List, Optional

from ...model.agent import Agent
from ...model.issue import Issue


class AssignmentStrategy(ABC):
    @abstractmethod
    def assign(self, agents: List[Agent], issue: Issue) -> Optional[Agent]:
        pass
