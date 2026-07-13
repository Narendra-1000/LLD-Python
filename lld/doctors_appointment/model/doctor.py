from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ..enums.specialization import Specialization


@dataclass
class Doctor:
    name: str
    specialization: Specialization
    rating: float
    id: UUID = field(default_factory=uuid4)
    availability: dict[str, bool] = field(default_factory=dict)
