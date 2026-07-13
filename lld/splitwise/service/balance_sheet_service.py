from ..model.group import Group
from ..model.split import Split
from ..model.user import User


class BalanceSheetService:
    def update_balances(
        self, group: Group, paid_by: User, splits: list[Split]
    ) -> None:
        total_amount = sum(split.amount for split in splits)
        group.get_balance_sheet(paid_by).add_total_paid(total_amount)

        for split in splits:
            user = split.user
            amt = split.amount
            group.get_balance_sheet(user).add_total_expense(amt)
            if user is not paid_by:
                group.get_balance_sheet(user).add_balance(paid_by, -amt)
                group.get_balance_sheet(paid_by).add_balance(user, amt)
