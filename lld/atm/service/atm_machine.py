from __future__ import annotations

from typing import Optional

from ..factory.atm_state_factory import ATMStateFactory
from ..model.atm import ATM
from ..model.card import Card
from ..repository.atm_repository import ATMRepository
from ..state.atm_state import ATMState


class ATMMachine:
    def __init__(self, atm_id: str, atm_repository: ATMRepository):
        self.atm_repository = atm_repository
        atm = atm_repository.get_by_id(atm_id)
        if atm is None:
            raise RuntimeError("ATM not found")
        self.atm: ATM = atm
        self.state: ATMState = ATMStateFactory.get_state(self.atm.status, self)
        self.current_card: Optional[Card] = None

    def insert_card(self, card: Card) -> None:
        self.state.insert_card(card)

    def enter_pin(self, pin: str) -> None:
        self.state.enter_pin(pin)

    def select_option(self, option: str) -> None:
        self.state.select_option(option)

    def dispense_cash(self, amount: int) -> None:
        self.state.dispense_cash(amount)

    def eject_card(self) -> None:
        self.state.eject_card()

    def set_state(self, state: ATMState) -> None:
        self.state = state
        self.atm.status = state.get_status()
        # persist the changes in db
