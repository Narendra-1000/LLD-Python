from dataclasses import dataclass, field
from uuid import UUID

from ..enums.specialization import Specialization
from ..model.doctor import Doctor


@dataclass
class DoctorRepository:
    doctor_map: dict[UUID, Doctor] = field(default_factory=dict)

    def save(self, doctor: Doctor) -> None:
        self.doctor_map[doctor.id] = doctor

    def find_by_id(self, doctor_id: UUID) -> Doctor | None:
        return self.doctor_map.get(doctor_id)

    def find_by_specialization(self, specialization: Specialization) -> list[Doctor]:
        return [
            doc
            for doc in self.doctor_map.values()
            if doc.specialization == specialization
        ]
