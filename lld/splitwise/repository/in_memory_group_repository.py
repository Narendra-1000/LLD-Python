from typing import Dict, Optional

from ..model.group import Group
from .group_repository import GroupRepository


class InMemoryGroupRepository(GroupRepository):
    def __init__(self) -> None:
        self._store: Dict[str, Group] = {}

    def find_by_id(self, id: str) -> Optional[Group]:
        return self._store.get(id)

    def save(self, group: Group) -> None:
        self._store[group.id] = group
