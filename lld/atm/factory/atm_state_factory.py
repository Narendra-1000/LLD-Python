from typing import TYPE_CHECKING

from ..enums.atm_status import ATMStatus
from ..state.atm_state import ATMState
from ..state.authenticated_state import AuthenticatedState
from ..state.card_inserted_state import CardInsertedState
from ..state.dispense_cash_state import DispenseCashState
from ..state.idle_state import IdleState

if TYPE_CHECKING:
    from ..service.atm_machine import ATMMachine


class ATMStateFactory:
    @staticmethod
    def get_state(status: ATMStatus, machine: "ATMMachine") -> ATMState:
        if status == ATMStatus.IDLE:
            return IdleState(machine)
        if status == ATMStatus.CARD_INSERTED:
            return CardInsertedState(machine)
        if status == ATMStatus.AUTHENTICATED:
            return AuthenticatedState(machine)
        if status == ATMStatus.DISPENSE_CASH:
            return DispenseCashState(machine)
        raise ValueError(f"Unknown ATM status: {status}")
