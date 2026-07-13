from abc import ABC
from dataclasses import dataclass, field

from ..enums.vehicle_status import VehicleStatus
from ..enums.vehicle_type import VehicleType
from .atomic_boolean import AtomicBoolean


@dataclass
class Vehicle(ABC):
    license_plate: str
    price_per_hour: float
    price_per_km: float
    type: VehicleType
    status: VehicleStatus = VehicleStatus.AVAILABLE
    booking_count: int = 0
    is_booked: AtomicBoolean = field(default_factory=AtomicBoolean, init=False, repr=False)

    def __post_init__(self) -> None:
        self.is_booked = AtomicBoolean(False)

    def increment_booking_count(self) -> None:
        self.booking_count += 1
