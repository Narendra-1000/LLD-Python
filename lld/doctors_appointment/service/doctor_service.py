from dataclasses import dataclass
from uuid import UUID

from ..enums.specialization import Specialization
from ..exception.doctor_not_found_exception import DoctorNotFoundException
from ..model.doctor import Doctor
from ..repository.doctor_repository import DoctorRepository


@dataclass
class DoctorService:
    repo: DoctorRepository

    def register(self, name: str, spec: Specialization, rating: float) -> Doctor:
        doctor = Doctor(name=name, specialization=spec, rating=rating)
        self.repo.save(doctor)
        return doctor

    def declare_availability(self, doctor_id: UUID, slots: list[str]) -> None:
        doc = self.repo.find_by_id(doctor_id)
        if doc is None:
            raise DoctorNotFoundException("Doctor not found")
        for slot in slots:
            doc.availability[slot] = True
