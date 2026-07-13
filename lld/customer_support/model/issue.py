import uuid
from dataclasses import dataclass, field
from typing import Optional

from ..enums.issue_status import IssueStatus
from ..enums.issue_type import IssueType


@dataclass
class Issue:
    transaction_id: str
    issue_type: IssueType
    subject: str
    description: str
    email: str
    id: str = field(init=False)
    status: IssueStatus = field(init=False, default=IssueStatus.OPEN)
    resolution: Optional[str] = None
    assigned_agent_id: Optional[str] = None

    def __post_init__(self) -> None:
        self.id = "I" + str(uuid.uuid4())[:6]

    def __str__(self) -> str:
        return (
            f'{self.id} {{"{self.transaction_id}", "{self.issue_type.name}", '
            f'"{self.subject}", "{self.description}", "{self.email}", '
            f'"{self.status.name}"}}'
        )
