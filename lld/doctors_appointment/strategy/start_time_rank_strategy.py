from ..dto.doctor_slot import DoctorSlot
from ..utils.utils import convert_string_to_local_time
from .slot_rank_strategy import SlotRankStrategy


class StartTimeRankStrategy(SlotRankStrategy):
    def rank(self, slots: list[DoctorSlot]) -> list[DoctorSlot]:
        slots.sort(key=lambda slot: convert_string_to_local_time(slot.slot))
        return slots
