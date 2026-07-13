from typing import Optional

from ..enums.atm_status import ATMStatus
from ..model.atm import ATM


class ATMRepository:
    def __init__(self):
        self._atms: dict[str, ATM] = {}

    def save(self, atm: ATM) -> None:
        self._atms[atm.id] = atm

    def get_by_id(self, id: str) -> Optional[ATM]:
        return self._atms.get(id)

    def update_atm_status_by_id(self, id: str, new_status: ATMStatus) -> None:
        self._atms[id].status = new_status
