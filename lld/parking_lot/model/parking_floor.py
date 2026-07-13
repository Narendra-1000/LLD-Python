from ..enums.vehicle_type import VehicleType
from .parking_spot import ParkingSpot


class ParkingFloor:
    def __init__(self, floor_id: str) -> None:
        self.id = floor_id
        self.spots: dict[str, ParkingSpot] = {}

    def add_spot(self, spot: ParkingSpot) -> None:
        self.spots[spot.id] = spot

    def find_available_spot(self, vehicle_type: VehicleType) -> ParkingSpot | None:
        for spot in self.spots.values():
            if spot.allowed_type == vehicle_type and spot.try_occupy():
                return spot
        return None
