from dataclasses import dataclass, field

from ..enums.vehicle_type import VehicleType
from .vehicle import Vehicle


@dataclass
class Branch:
    id: str
    city: str
    vehicles: dict[VehicleType, list[Vehicle]] = field(default_factory=dict)

    def get_vehicles_by_type(self, vehicle_type: VehicleType) -> list[Vehicle]:
        return list(self.vehicles.get(vehicle_type, []))

    def add_vehicle(self, vehicle: Vehicle) -> None:
        self.vehicles.setdefault(vehicle.type, []).append(vehicle)

    def remove_vehicle(self, vehicle: Vehicle) -> None:
        vehicle_list = self.vehicles.get(vehicle.type)
        if vehicle_list is not None:
            vehicle_list.remove(vehicle)
