from ..model.atm import ATM
from .cash_dispenser import CashDispenser


class OneHundredDispenser(CashDispenser):
    def __init__(self):
        self._next: CashDispenser | None = None

    def set_next_dispenser(self, next_dispenser: CashDispenser) -> None:
        self._next = next_dispenser

    def can_dispense(self, atm: ATM, amount: int) -> bool:
        available_notes = atm.one_hundred_count
        notes = min(amount // 100, available_notes)
        remainder = amount - notes * 100
        return remainder == 0

    def dispense(self, atm: ATM, amount: int) -> None:
        available_notes = atm.one_hundred_count
        notes = min(amount // 100, available_notes)
        atm.one_hundred_count = available_notes - notes
        if notes > 0:
            print(f"Dispensed {notes} x ₹100 notes")
