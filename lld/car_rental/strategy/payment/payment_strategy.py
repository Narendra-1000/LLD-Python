from abc import ABC, abstractmethod

from ...model.booking import Booking


class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, booking: Booking) -> bool:
        pass
