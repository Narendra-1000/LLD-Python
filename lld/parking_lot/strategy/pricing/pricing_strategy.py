from abc import ABC, abstractmethod
from datetime import datetime

from ...enums.vehicle_type import VehicleType


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(
        self,
        vehicle_type: VehicleType,
        entry_time: datetime,
        exit_time: datetime,
    ) -> float:
        pass
