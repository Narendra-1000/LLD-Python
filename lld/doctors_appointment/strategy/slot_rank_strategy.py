from abc import ABC, abstractmethod

from ..dto.doctor_slot import DoctorSlot


class SlotRankStrategy(ABC):
    @abstractmethod
    def rank(self, slots: list[DoctorSlot]) -> list[DoctorSlot]:
        pass
