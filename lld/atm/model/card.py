from dataclasses import dataclass

from .account import Account


@dataclass
class Card:
    card_number: str
    pin: str
    account: Account
