from __future__ import annotations

from typing import TYPE_CHECKING

from ..cor.cash_dispenser import CashDispenser
from ..cor.cash_dispenser_chain_builder import CashDispenserChainBuilder
from ..enums.atm_status import ATMStatus
from ..model.card import Card
from .atm_state import ATMState

if TYPE_CHECKING:
    from ..service.atm_machine import ATMMachine


class DispenseCashState(ATMState):
    def __init__(self, atm_machine: ATMMachine):
        self._atm_machine = atm_machine
        self._chain: CashDispenser = CashDispenserChainBuilder.build_chain()

    def insert_card(self, card: Card) -> None:
        print("Transaction in progress. Cannot insert another card.")

    def enter_pin(self, pin: str) -> None:
        print("Already authenticated.")

    def select_option(self, option: str) -> None:
        print("Option already selected.")

    def dispense_cash(self, amount: int) -> None:
        atm_balance = self._atm_machine.atm.cash_available
        account_balance = self._atm_machine.current_card.account.balance

        if amount > atm_balance:
            print(f"ATM has insufficient cash. Cannot dispense {amount}")
            self.eject_card()
            return

        if amount > account_balance:
            print("Insufficient account balance.")
            self.eject_card()
            return

        # Now check if note combination is possible
        if self._chain.can_dispense(self._atm_machine.atm, amount):
            self._chain.dispense(self._atm_machine.atm, amount)

            # Deduct from ATM cash & account balance
            self._atm_machine.atm.cash_available = atm_balance - amount
            self._atm_machine.current_card.account.balance = account_balance - amount

            self.eject_card()
            print(f"Cash dispensed: {amount}")
        else:
            print("Cannot dispense requested amount with available denominations.")
            self.eject_card()

    def eject_card(self) -> None:
        from .idle_state import IdleState

        self._atm_machine.current_card = None
        print("Card ejected.")
        self._atm_machine.set_state(IdleState(self._atm_machine))  # use factory

    def get_status(self) -> ATMStatus:
        return ATMStatus.DISPENSE_CASH
