from ..model.atm import ATM
from .cash_dispenser import CashDispenser


class FiveHundredDispenser(CashDispenser):
    def __init__(self):
        self._next: CashDispenser | None = None

    def set_next_dispenser(self, next_dispenser: CashDispenser) -> None:
        self._next = next_dispenser

    def can_dispense(self, atm: ATM, amount: int) -> bool:
        available_notes = atm.five_hundred_count
        notes = min(amount // 500, available_notes)
        remainder = amount - notes * 500
        return remainder == 0 or (
            self._next is not None and self._next.can_dispense(atm, remainder)
        )

    def dispense(self, atm: ATM, amount: int) -> None:
        available_notes = atm.five_hundred_count
        notes = min(amount // 500, available_notes)
        atm.five_hundred_count = available_notes - notes
        remainder = amount - notes * 500

        if notes > 0:
            print(f"Dispensed {notes} x ₹500 notes")

        if remainder > 0 and self._next is not None:
            self._next.dispense(atm, remainder)
