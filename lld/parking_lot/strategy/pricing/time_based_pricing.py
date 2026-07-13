import math
from datetime import datetime, time, timedelta

from ...enums.vehicle_type import VehicleType
from .pricing_strategy import PricingStrategy


class TimeBasedPricing(PricingStrategy):
    PEAK_START = time(8, 0)
    PEAK_END = time(17, 0)

    def _is_peak(self, t: time) -> bool:
        return self.PEAK_START <= t <= self.PEAK_END

    def calculate_fee(
        self,
        vehicle_type: VehicleType,
        entry_time: datetime,
        exit_time: datetime,
    ) -> float:
        if exit_time < entry_time:
            raise ValueError("Exit time before entry time")

        duration_minutes = int((exit_time - entry_time).total_seconds() // 60)
        total_hours = math.ceil(duration_minutes / 60.0)

        peak_hours = 0
        non_peak_hours = 0

        cursor = entry_time.replace(minute=0, second=0, microsecond=0)
        for _ in range(int(total_hours)):
            hour_start = cursor.time()
            if self._is_peak(hour_start):
                peak_hours += 1
            else:
                non_peak_hours += 1
            cursor += timedelta(hours=1)

        peak_rate = {
            VehicleType.CAR: 30.0,
            VehicleType.BIKE: 15.0,
            VehicleType.TRUCK: 50.0,
        }[vehicle_type]

        non_peak_rate = {
            VehicleType.CAR: 20.0,
            VehicleType.BIKE: 10.0,
            VehicleType.TRUCK: 30.0,
        }[vehicle_type]

        return peak_hours * peak_rate + non_peak_hours * non_peak_rate
