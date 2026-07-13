from abc import ABC, abstractmethod

from ...model.vehicle import Vehicle


class BookingStrategy(ABC):
    @abstractmethod
    def book_vehicle(self, vehicles: list[Vehicle]) -> Vehicle | None:
        pass
