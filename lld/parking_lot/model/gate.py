from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..enums.gate_type import GateType


@dataclass
class Gate(ABC):
    id: str

    @abstractmethod
    def get_type(self) -> GateType:
        pass
