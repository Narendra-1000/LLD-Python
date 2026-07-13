import uuid
from typing import Dict, List, Optional

from ..enums.split_type import SplitType
from ..model.group import Group
from ..model.user import User
from ..repository.group_repository import GroupRepository
from .debt_simplification_service import DebtSimplificationService
from .expense_service import ExpenseService


class GroupService:
    def __init__(
        self,
        repo: GroupRepository,
        expense_service: ExpenseService,
        simplifier: DebtSimplificationService,
    ) -> None:
        self._repo = repo
        self._expense_service = expense_service
        self._simplifier = simplifier

    def create_group(self, name: str, members: List[User]) -> str:
        group_id = str(uuid.uuid4())
        group = Group(group_id, name)
        for member in members:
            group.add_member(member)

        self._repo.save(group)
        return group_id

    def add_member(self, group_id: str, user: User) -> None:
        self._get(group_id).add_member(user)

    def add_expense(
        self,
        group_id: str,
        description: str,
        amount: float,
        paid_by: User,
        participants: List[User],
        split_type: SplitType,
        meta: Optional[Dict[User, float]],
    ) -> None:
        self._expense_service.add_expense(
            self._get(group_id),
            description,
            amount,
            paid_by,
            participants,
            split_type,
            meta,
        )

    def simplify_debts(self, group_id: str) -> None:
        self._simplifier.simplify_debts(self._get(group_id))

    def print_balances(self, group_id: str) -> None:
        group = self._get(group_id)
        for user in group.members:
            sheet = group.get_balance_sheet(user)

            owe = 0.0
            get = 0.0
            for value in sheet.balances.values():
                if value < 0:
                    owe += -value
                else:
                    get += value

            print(
                f"                               💵 {user.name}\n"
                f"                               Paid: {sheet.total_paid:.2f}  "
                f"Expense: {sheet.total_expense:.2f}\n"
                f"                               You owe: {owe:.2f}, You get: {get:.2f}"
            )

            for other, val in sheet.balances.items():
                direction = "← get" if val > 0 else "→ owe"
                print(f"  {direction} {abs(val):.2f} {other.name}")
            print("--------------------------")

    def _get(self, group_id: str) -> Group:
        group = self._repo.find_by_id(group_id)
        if group is None:
            raise ValueError(f"Group not found: {group_id}")
        return group
