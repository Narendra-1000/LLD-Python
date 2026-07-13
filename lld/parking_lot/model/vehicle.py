from abc import ABC
from dataclasses import dataclass

from ..enums.vehicle_type import VehicleType


@dataclass
class Vehicle(ABC):
    number: str
    type: VehicleType
