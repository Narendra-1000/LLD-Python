from typing import List, Optional

from ...model.agent import Agent
from ...model.issue import Issue
from .assignment_strategy import AssignmentStrategy


class DefaultAssignmentStrategy(AssignmentStrategy):
    def assign(self, agents: List[Agent], issue: Issue) -> Optional[Agent]:
        for agent in agents:
            if agent.is_available() and issue.issue_type in agent.expertise:
                return agent
        return None
