import math
from datetime import datetime

from ...model.vehicle import Vehicle
from .pricing_strategy import PricingStrategy


class HourlyPricingStrategy(PricingStrategy):
    def calculate_price(
        self,
        vehicle: Vehicle,
        start: datetime,
        end: datetime,
        distance_km: float,
    ) -> float:
        minutes = int((end - start).total_seconds() // 60)
        hours = math.ceil(minutes / 60.0)
        return vehicle.price_per_hour * hours
