from abc import ABC, abstractmethod

from ..enums.atm_status import ATMStatus
from ..model.card import Card


class ATMState(ABC):
    @abstractmethod
    def insert_card(self, card: Card) -> None:
        pass

    @abstractmethod
    def enter_pin(self, pin: str) -> None:
        pass

    @abstractmethod
    def select_option(self, option: str) -> None:
        pass

    @abstractmethod
    def dispense_cash(self, amount: int) -> None:
        pass

    @abstractmethod
    def eject_card(self) -> None:
        pass

    @abstractmethod
    def get_status(self) -> ATMStatus:
        pass
