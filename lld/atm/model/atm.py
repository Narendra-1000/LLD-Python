from dataclasses import dataclass

from ..enums.atm_status import ATMStatus


@dataclass
class ATM:
    id: str
    status: ATMStatus = ATMStatus.IDLE
    cash_available: float = 0.0
    two_thousand_count: int = 0
    five_hundred_count: int = 0
    one_hundred_count: int = 0

    def __init__(
        self,
        id: str,
        two_thousand_count: int,
        five_hundred_count: int,
        one_hundred_count: int,
    ):
        self.id = id
        self.cash_available = (
            2000 * two_thousand_count
            + 500 * five_hundred_count
            + 100 * one_hundred_count
        )
        self.status = ATMStatus.IDLE
        self.two_thousand_count = two_thousand_count
        self.five_hundred_count = five_hundred_count
        self.one_hundred_count = one_hundred_count
