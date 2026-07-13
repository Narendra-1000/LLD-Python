from ..model.atm import ATM
from .cash_dispenser import CashDispenser


class TwoThousandDispenser(CashDispenser):
    def __init__(self):
        self._next: CashDispenser | None = None

    def set_next_dispenser(self, next_dispenser: CashDispenser) -> None:
        self._next = next_dispenser

    def can_dispense(self, atm: ATM, amount: int) -> bool:
        count = atm.two_thousand_count
        notes = min(amount // 2000, count)
        remainder = amount - notes * 2000
        return remainder == 0 or (
            self._next is not None and self._next.can_dispense(atm, remainder)
        )

    def dispense(self, atm: ATM, amount: int) -> None:
        count = atm.two_thousand_count
        notes = min(amount // 2000, count)
        atm.two_thousand_count = count - notes

        remainder = amount - notes * 2000
        if notes > 0:
            print(f"Dispensed {notes} x 2000 notes")

        if remainder > 0 and self._next is not None:
            self._next.dispense(atm, remainder)
