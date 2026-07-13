from typing import Dict

from .user import User


class BalanceSheet:
    def __init__(self) -> None:
        self.total_paid: float = 0.0
        self.total_expense: float = 0.0
        self.balances: Dict[User, float] = {}

    def add_total_paid(self, amount: float) -> None:
        self.total_paid += amount

    def add_total_expense(self, amount: float) -> None:
        self.total_expense += amount

    def add_balance(self, other: User, amount: float) -> None:
        self.balances[other] = self.balances.get(other, 0.0) + amount
        if abs(self.balances[other]) < 1e-6:
            del self.balances[other]

    def clear_balances(self) -> None:
        self.balances.clear()

    def print(self, me: User) -> None:
        you_owe = 0.0
        you_get_back = 0.0
        for amount in self.balances.values():
            if amount < 0:
                you_owe += -amount
            else:
                you_get_back += amount

        print(f"💵 Balance sheet of : {me.name}")
        print(f"Total You Paid : {self.total_paid}")
        print(f"Total Expense : {self.total_expense}")
        print(f"Total You Owe : {you_owe}")
        print(f"Total You Get Back : {you_get_back}")

        for other, amount in self.balances.items():
            if amount > 0:
                print(f"You get back {amount} from {other.name}")
            elif amount < 0:
                print(f"You owe {-amount} to {other.name}")
        print("---------------------------------")
        print("---------------------------------")
