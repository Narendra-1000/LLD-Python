from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Booking:
    patient_id: UUID
    doctor_id: UUID
    slot: str
    id: UUID = field(default_factory=uuid4)
