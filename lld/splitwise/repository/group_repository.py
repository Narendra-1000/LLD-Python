from abc import ABC, abstractmethod
from typing import Optional

from ..model.group import Group


class GroupRepository(ABC):
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Group]:
        pass

    @abstractmethod
    def save(self, group: Group) -> None:
        pass
