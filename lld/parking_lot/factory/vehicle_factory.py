from ..enums.vehicle_type import VehicleType
from ..model.bike import Bike
from ..model.car import Car
from ..model.truck import Truck
from ..model.vehicle import Vehicle


class VehicleFactory:
    @staticmethod
    def create(number: str, vehicle_type: VehicleType) -> Vehicle:
        if vehicle_type == VehicleType.CAR:
            return Car(number)
        if vehicle_type == VehicleType.BIKE:
            return Bike(number)
        if vehicle_type == VehicleType.TRUCK:
            return Truck(number)
        raise ValueError(f"Unsupported vehicle type: {vehicle_type}")
