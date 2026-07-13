from .cash_dispenser import CashDispenser
from .five_hundred_dispenser import FiveHundredDispenser
from .one_hundred_dispenser import OneHundredDispenser
from .two_thousand_dispenser import TwoThousandDispenser


class CashDispenserChainBuilder:
    @staticmethod
    def build_chain() -> CashDispenser:
        d1 = TwoThousandDispenser()
        d2 = FiveHundredDispenser()
        d3 = OneHundredDispenser()

        d1.set_next_dispenser(d2)
        d2.set_next_dispenser(d3)
        return d1
