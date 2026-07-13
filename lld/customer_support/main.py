from .enums.issue_status import IssueStatus
from .enums.issue_type import IssueType
from .repository.agent_repository import AgentRepository
from .repository.issue_repository import IssueRepository
from .service.agent_service import AgentService
from .service.assignment_service import AssignmentService
from .service.issue_service import IssueService
from .strategy.assignment.default_assignment_strategy import DefaultAssignmentStrategy


def main() -> None:
    agent_repository = AgentRepository()
    issue_repository = IssueRepository()

    agent_service = AgentService(agent_repository)
    issue_service = IssueService(issue_repository, agent_repository)
    assignment_service = AssignmentService(
        agent_repository, issue_repository, DefaultAssignmentStrategy()
    )

    i1 = issue_service.create_issue(
        "T1",
        IssueType.PAYMENT_RELATED,
        "Payment Failed",
        "My payment failed but money is debited",
        "testUser1@test.com",
    )
    i2 = issue_service.create_issue(
        "T2",
        IssueType.MUTUAL_FUND_RELATED,
        "Purchase Failed",
        "Unable to purchase Mutual Fund",
        "testUser2@test.com",
    )
    i3 = issue_service.create_issue(
        "T3",
        IssueType.PAYMENT_RELATED,
        "Payment Failed",
        "My payment failed but money is debited",
        "testUser2@test.com",
    )

    agent_service.add_agent(
        "agent1@test.com",
        "Agent 1",
        [IssueType.PAYMENT_RELATED, IssueType.GOLD_RELATED],
    )
    agent_service.add_agent(
        "agent2@test.com",
        "Agent 2",
        [IssueType.PAYMENT_RELATED],
    )

    assignment_service.assign_issue(i1.id)
    assignment_service.assign_issue(i2.id)
    assignment_service.assign_issue(i3.id)

    print("\n--- Issues for testUser2@test.com ---")
    for issue in issue_service.get_issues({"email": "testUser2@test.com"}):
        print(issue)

    print("\n--- Payment Related Issues ---")
    for issue in issue_service.get_issues({"type": "Payment Related"}):
        print(issue)

    issue_service.update_issue(
        i3.id, IssueStatus.IN_PROGRESS, "Waiting for payment confirmation"
    )

    issue_service.resolve_issue(
        i3.id, "Payment failed. Debited amount will be reversed."
    )

    print("\n--- Agent Work History ---")
    agent_service.view_agents_work_history()


if __name__ == "__main__":
    main()
