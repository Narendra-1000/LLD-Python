from abc import ABC, abstractmethod

from ..model.atm import ATM


class CashDispenser(ABC):
    @abstractmethod
    def set_next_dispenser(self, next_dispenser: "CashDispenser") -> None:
        pass

    @abstractmethod
    def can_dispense(self, atm: ATM, amount: int) -> bool:
        pass

    @abstractmethod
    def dispense(self, atm: ATM, amount: int) -> None:
        pass
