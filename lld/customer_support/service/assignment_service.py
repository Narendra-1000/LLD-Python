from typing import List

from ..enums.issue_status import IssueStatus
from ..model.agent import Agent
from ..repository.agent_repository import AgentRepository
from ..repository.issue_repository import IssueRepository
from ..strategy.assignment.assignment_strategy import AssignmentStrategy


class AssignmentService:
    def __init__(
        self,
        agent_repository: AgentRepository,
        issue_repository: IssueRepository,
        strategy: AssignmentStrategy,
    ) -> None:
        self._agent_repository = agent_repository
        self._issue_repository = issue_repository
        self._strategy = strategy

    def assign_issue(self, issue_id: str) -> None:
        issue = self._issue_repository.get_by_id(issue_id)
        if issue is None:
            raise ValueError("Issue not found")

        agents: List[Agent] = list(self._agent_repository.get_all())
        assigned = self._strategy.assign(agents, issue)

        if assigned is not None:
            assigned.assigned_issue_id = issue.id
            issue.assigned_agent_id = assigned.id
            print(f">>> Issue {issue_id} assigned to agent {assigned.id}")
        else:
            for agent in agents:
                if issue.issue_type in agent.expertise:
                    agent.wait_list.append(issue.id)
                    issue.status = IssueStatus.WAITING
                    print(f">>> Issue {issue_id} added to waitlist of Agent {agent.id}")
                    return
            print(f">>> No agent found with expertise for issue {issue_id}")
