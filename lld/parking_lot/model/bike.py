from ..enums.vehicle_type import VehicleType
from .vehicle import Vehicle


class Bike(Vehicle):
    def __init__(self, number: str) -> None:
        super().__init__(number=number, type=VehicleType.BIKE)
