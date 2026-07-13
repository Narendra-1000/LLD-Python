from datetime import datetime

from ..enums.booking_status import BookingStatus
from ..model.booking import Booking


class VehicleAvailabilityChecker:
    @staticmethod
    def is_available(
        bookings: list[Booking],
        start: datetime,
        end: datetime,
    ) -> bool:
        active_bookings = sorted(
            [
                booking
                for booking in bookings
                if booking.status in (BookingStatus.CREATED, BookingStatus.CONFIRMED)
            ],
            key=lambda booking: booking.start_time,
        )

        for booking in active_bookings:
            existing_start = booking.start_time
            existing_end = booking.end_time

            overlaps = not (end < existing_start or start > existing_end)
            if overlaps:
                return False

        return True
