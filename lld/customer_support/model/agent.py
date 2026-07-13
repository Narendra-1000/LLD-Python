from collections import deque
from dataclasses import dataclass, field
from typing import Optional, Set

from ..enums.issue_type import IssueType


@dataclass
class Agent:
    id: str
    email: str
    name: str
    expertise: Set[IssueType]
    assigned_issue_id: Optional[str] = None
    wait_list: deque = field(default_factory=deque)
    history: list = field(default_factory=list)

    def is_available(self) -> bool:
        return self.assigned_issue_id is None
