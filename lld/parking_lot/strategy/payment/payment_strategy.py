from abc import ABC, abstractmethod

from ...model.ticket import Ticket


class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, ticket: Ticket, amount: float) -> bool:
        pass
