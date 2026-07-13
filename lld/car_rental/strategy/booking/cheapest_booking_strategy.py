from ...enums.pricing_strategy_type import PricingStrategyType
from ...model.vehicle import Vehicle
from .booking_strategy import BookingStrategy


class CheapestBookingStrategy(BookingStrategy):
    def __init__(self, pricing_type: PricingStrategyType) -> None:
        self._pricing_type = pricing_type

    def book_vehicle(self, vehicles: list[Vehicle]) -> Vehicle | None:
        sorted_vehicles = sorted(
            vehicles,
            key=lambda vehicle: (
                vehicle.price_per_hour
                if self._pricing_type == PricingStrategyType.TIME_BASED
                else vehicle.price_per_km
            ),
        )

        for vehicle in sorted_vehicles:
            if vehicle.is_booked.compare_and_set(False, True):
                return vehicle

        return None
