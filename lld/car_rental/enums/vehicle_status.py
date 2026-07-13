from enum import Enum


class VehicleStatus(Enum):
    AVAILABLE = "AVAILABLE"
    BOOKED = "BOOKED"
    IN_SERVICE = "IN_SERVICE"
    DECOMMISSIONED = "DECOMMISSIONED"
