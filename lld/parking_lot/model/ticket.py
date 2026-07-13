from dataclasses import dataclass, field
from datetime import datetime

from ..enums.payment_status import PaymentStatus
from .vehicle import Vehicle


@dataclass
class Ticket:
    ticket_id: str
    entry_time: datetime
    vehicle: Vehicle
    floor_id: str
    spot_id: str
    payment_status: PaymentStatus = field(default=PaymentStatus.PENDING)
