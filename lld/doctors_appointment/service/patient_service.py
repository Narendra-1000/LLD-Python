from dataclasses import dataclass
from uuid import UUID

from ..exception.patient_not_found_exception import PatientNotFoundException
from ..model.patient import Patient
from ..repository.patient_repository import PatientRepository


@dataclass
class PatientService:
    repo: PatientRepository

    def register(self, name: str) -> Patient:
        patient = Patient(name=name)
        self.repo.save(patient)
        return patient

    def find_by_id(self, patient_id: UUID) -> Patient:
        patient = self.repo.find_by_id(patient_id)
        if patient is None:
            raise PatientNotFoundException("Patient not found")
        return patient
