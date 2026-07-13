from dataclasses import dataclass

from ..model.doctor import Doctor


@dataclass
class DoctorSlot:
    doctor: Doctor
    slot: str
