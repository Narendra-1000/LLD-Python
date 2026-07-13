from ..dto.doctor_slot import DoctorSlot
from .slot_rank_strategy import SlotRankStrategy


class RatingBasedRankStrategy(SlotRankStrategy):
    def rank(self, slots: list[DoctorSlot]) -> list[DoctorSlot]:
        slots.sort(key=lambda slot: slot.doctor.rating, reverse=True)
        return slots
