from typing import Dict, List, Optional

from ..enums.split_type import SplitType
from ..factory.split_strategy_factory import SplitStrategyFactory
from ..model.expense import Expense
from ..model.group import Group
from ..model.user import User
from .balance_sheet_service import BalanceSheetService


class ExpenseService:
    def __init__(self, balance_sheet_service: BalanceSheetService) -> None:
        self._balance_sheet_service = balance_sheet_service

    def add_expense(
        self,
        group: Group,
        description: str,
        amount: float,
        paid_by: User,
        participants: List[User],
        split_type: SplitType,
        metadata: Optional[Dict[User, float]],
    ) -> None:
        if metadata is None:
            metadata = {}
        strategy = SplitStrategyFactory.get_strategy(split_type)
        splits = strategy.split(amount, participants, metadata)
        expense = Expense(description, amount, paid_by, splits, split_type)
        group.add_expense(expense)

        self._balance_sheet_service.update_balances(group, paid_by, splits)
