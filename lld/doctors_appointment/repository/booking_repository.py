from collections import deque
from dataclasses import dataclass, field
from uuid import UUID

from ..model.booking import Booking


@dataclass
class BookingRepository:
    booking_map: dict[UUID, Booking] = field(default_factory=dict)
    waitlist: dict[str, deque[UUID]] = field(default_factory=dict)

    def save(self, booking: Booking) -> None:
        self.booking_map[booking.id] = booking

    def delete(self, booking: Booking) -> None:
        del self.booking_map[booking.id]

    def get_booking_by_id(self, booking_id: UUID) -> Booking | None:
        return self.booking_map.get(booking_id)

    def find_by_doctor(self, doctor_id: UUID) -> list[Booking]:
        return [b for b in self.booking_map.values() if b.doctor_id == doctor_id]

    def find_by_patient(self, patient_id: UUID) -> list[Booking]:
        return [b for b in self.booking_map.values() if b.patient_id == patient_id]

    def add_to_waitlist(self, doctor_slot_key: str, patient_id: UUID) -> None:
        if doctor_slot_key not in self.waitlist:
            self.waitlist[doctor_slot_key] = deque()
        self.waitlist[doctor_slot_key].append(patient_id)

    def pop_from_waitlist(self, doctor_slot_key: str) -> UUID | None:
        queue = self.waitlist.get(doctor_slot_key)
        if queue is None:
            return None
        return queue.popleft() if queue else None
