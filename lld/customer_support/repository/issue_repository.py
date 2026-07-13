from typing import Collection, Dict, Optional

from ..model.issue import Issue


class IssueRepository:
    def __init__(self) -> None:
        self._issues: Dict[str, Issue] = {}

    def save(self, issue: Issue) -> None:
        self._issues[issue.id] = issue

    def get_by_id(self, id: str) -> Optional[Issue]:
        return self._issues.get(id)

    def get_all(self) -> Collection[Issue]:
        return self._issues.values()
