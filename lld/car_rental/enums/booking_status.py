from enum import Enum


class BookingStatus(Enum):
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
