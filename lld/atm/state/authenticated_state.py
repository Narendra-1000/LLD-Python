from __future__ import annotations

from typing import TYPE_CHECKING

from ..enums.atm_status import ATMStatus
from ..model.card import Card
from .atm_state import ATMState

if TYPE_CHECKING:
    from ..service.atm_machine import ATMMachine


class AuthenticatedState(ATMState):
    def __init__(self, atm_machine: ATMMachine):
        self._atm_machine = atm_machine

    def insert_card(self, card: Card) -> None:
        print("Card already inserted.")

    def enter_pin(self, pin: str) -> None:
        print("Already authenticated.")

    def select_option(self, option: str) -> None:
        from .dispense_cash_state import DispenseCashState

        # can add options like deposit, check balance based on option selected.
        print("Option selected: Withdrawal.")
        self._atm_machine.set_state(DispenseCashState(self._atm_machine))

    def dispense_cash(self, amount: int) -> None:
        print("Select an option first.")

    def eject_card(self) -> None:
        from .idle_state import IdleState

        self._atm_machine.current_card = None
        print("Card ejected.")
        self._atm_machine.set_state(IdleState(self._atm_machine))

    def get_status(self) -> ATMStatus:
        return ATMStatus.AUTHENTICATED
