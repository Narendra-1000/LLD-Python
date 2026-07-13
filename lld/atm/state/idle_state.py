from __future__ import annotations

from typing import TYPE_CHECKING

from ..enums.atm_status import ATMStatus
from ..model.card import Card
from .atm_state import ATMState

if TYPE_CHECKING:
    from ..service.atm_machine import ATMMachine


class IdleState(ATMState):
    def __init__(self, atm_machine: ATMMachine):
        self._atm_machine = atm_machine

    def insert_card(self, card: Card) -> None:
        from .card_inserted_state import CardInsertedState

        self._atm_machine.current_card = card
        print("Card inserted.")
        self._atm_machine.set_state(CardInsertedState(self._atm_machine))

    def enter_pin(self, pin: str) -> None:
        print("No card inserted.")

    def select_option(self, option: str) -> None:
        print("No card inserted.")

    def dispense_cash(self, amount: int) -> None:
        print("No card inserted.")

    def eject_card(self) -> None:
        print("No card to eject.")

    def get_status(self) -> ATMStatus:
        return ATMStatus.IDLE
