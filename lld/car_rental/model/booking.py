from dataclasses import dataclass
from datetime import datetime

from ..enums.booking_status import BookingStatus
from ..enums.payment_status import PaymentStatus
from .branch import Branch
from .user import User
from .vehicle import Vehicle


def _format_datetime(value: datetime) -> str:
    hour = value.hour % 12 or 12
    return f"{value.day} {value.strftime('%b')} {hour}:{value.strftime('%M %p %Y')}"


@dataclass
class Booking:
    booking_id: str
    user: User
    vehicle: Vehicle
    pickup_branch: Branch
    drop_branch: Branch
    start_time: datetime
    end_time: datetime
    status: BookingStatus = BookingStatus.CREATED
    payment_status: PaymentStatus = PaymentStatus.PENDING
    amount: float = 0.0

    def __str__(self) -> str:
        return (
            "\n"
            f"Booking ID: {self.booking_id}\n"
            f"User: {self.user.name if self.user else 'N/A'}\n"
            f"Pickup Time: {_format_datetime(self.start_time)}\n"
            f"Drop Time: {_format_datetime(self.end_time)}\n"
            f"Pickup Location: {self.pickup_branch.city if self.pickup_branch else 'N/A'}\n"
            f"Drop Location: {self.drop_branch.city if self.drop_branch else 'N/A'}\n"
            f"Vehicle Type: {self.vehicle.type.name if self.vehicle else 'N/A'}\n"
            f"Vehicle Number Plate: {self.vehicle.license_plate if self.vehicle else 'N/A'}\n"
            f"Amount: ${self.amount:.2f}\n"
            f"Status: {self.status.name}\n"
        )
