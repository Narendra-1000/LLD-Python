from dataclasses import dataclass, field
from uuid import UUID

from ..model.patient import Patient


@dataclass
class PatientRepository:
    patient_map: dict[UUID, Patient] = field(default_factory=dict)

    def save(self, patient: Patient) -> None:
        self.patient_map[patient.id] = patient

    def find_by_id(self, patient_id: UUID) -> Patient | None:
        return self.patient_map.get(patient_id)
