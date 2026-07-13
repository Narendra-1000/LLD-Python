from ...model.vehicle import Vehicle
from .booking_strategy import BookingStrategy


class LeastBookedVehicleStrategy(BookingStrategy):
    def book_vehicle(self, vehicles: list[Vehicle]) -> Vehicle | None:
        sorted_vehicles = sorted(vehicles, key=lambda vehicle: vehicle.booking_count)

        for vehicle in sorted_vehicles:
            if vehicle.is_booked.compare_and_set(False, True):
                return vehicle

        return None
