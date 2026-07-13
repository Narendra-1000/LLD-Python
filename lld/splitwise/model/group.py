from typing import Dict, List

from .balance_sheet import BalanceSheet
from .expense import Expense
from .user import User


class Group:
    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name
        self.members: List[User] = []
        self.expenses: List[Expense] = []
        self.balance_sheets: Dict[User, BalanceSheet] = {}

    def add_member(self, user: User) -> None:
        self.members.append(user)
        self.balance_sheets.setdefault(user, BalanceSheet())

    def add_expense(self, expense: Expense) -> None:
        self.expenses.append(expense)

    def get_balance_sheet(self, user: User) -> BalanceSheet:
        return self.balance_sheets[user]
