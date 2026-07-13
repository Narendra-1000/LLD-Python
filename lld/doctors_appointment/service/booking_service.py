from dataclasses import dataclass
from uuid import UUID

from ..dto.doctor_slot import DoctorSlot
from ..enums.specialization import Specialization
from ..exception.booking_not_found_exception import BookingNotFoundException
from ..model.booking import Booking
from ..repository.booking_repository import BookingRepository
from ..repository.doctor_repository import DoctorRepository
from ..repository.patient_repository import PatientRepository
from ..strategy.slot_rank_strategy import SlotRankStrategy


@dataclass
class BookingService:
    booking_repo: BookingRepository
    doctor_repo: DoctorRepository
    patient_repo: PatientRepository

    def search(self, spec: Specialization, strategy: SlotRankStrategy) -> list[DoctorSlot]:
        doctors = self.doctor_repo.find_by_specialization(spec)
        result: list[DoctorSlot] = []

        for doctor in doctors:
            for slot, is_available in doctor.availability.items():
                if is_available:
                    result.append(DoctorSlot(doctor=doctor, slot=slot))

        return strategy.rank(result)

    def book(self, patient_id: UUID, doctor_id: UUID, slot: str) -> Booking:
        doctor = self.doctor_repo.find_by_id(doctor_id)
        availability = doctor.availability

        if slot not in availability:
            raise RuntimeError(
                "Invalid slot: Doctor has not declared availability for this slot."
            )

        for booking in self.booking_repo.find_by_patient(patient_id):
            if booking.slot == slot:
                raise RuntimeError("Patient already has an appointment at this time")

        if availability[slot]:
            booking = Booking(patient_id=patient_id, doctor_id=doctor_id, slot=slot)
            self.booking_repo.save(booking)
            availability[slot] = False

            patient = self.patient_repo.find_by_id(patient_id)
            print(
                f"\n{patient.name} booked a slot successfully for slot : {slot}"
            )

            return booking

        key = f"{doctor_id}-{slot}"
        self.booking_repo.add_to_waitlist(key, patient_id)
        raise RuntimeError("Slot already booked. Added to waitlist.")

    def cancel(self, booking_id: UUID) -> None:
        booking = self.booking_repo.get_booking_by_id(booking_id)
        if booking is None:
            raise BookingNotFoundException("Booking not found")

        doctor = self.doctor_repo.find_by_id(booking.doctor_id)
        doctor.availability[booking.slot] = True
        self.booking_repo.delete(booking)

        patient = self.patient_repo.find_by_id(booking.patient_id)
        print(
            f"\n{patient.name} cancelled the booking for slot : {booking.slot}"
        )

        key = f"{doctor.id}-{booking.slot}"
        next_patient = self.booking_repo.pop_from_waitlist(key)
        if next_patient is not None:
            self.book(next_patient, doctor.id, booking.slot)

    def view_bookings_by_doctor(self, doctor_id: UUID) -> list[Booking]:
        return self.booking_repo.find_by_doctor(doctor_id)

    def view_bookings_by_patient(self, patient_id: UUID) -> list[Booking]:
        return self.booking_repo.find_by_patient(patient_id)
