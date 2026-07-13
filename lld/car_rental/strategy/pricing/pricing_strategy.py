from abc import ABC, abstractmethod
from datetime import datetime

from ...model.vehicle import Vehicle


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(
        self,
        vehicle: Vehicle,
        start: datetime,
        end: datetime,
        distance_km: float,
    ) -> float:
        pass
