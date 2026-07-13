from .enums.split_type import SplitType
from .model.user import User
from .repository.in_memory_group_repository import InMemoryGroupRepository
from .service.balance_sheet_service import BalanceSheetService
from .service.debt_simplification_service import DebtSimplificationService
from .service.expense_service import ExpenseService
from .service.group_service import GroupService


def main() -> None:
    shubh = User("u1", "Shubh")
    bob = User("u2", "Bob")
    tom = User("u3", "Tom")
    jake = User("u4", "Jake")

    repo = InMemoryGroupRepository()
    balance_sheet_service = BalanceSheetService()
    expense_service = ExpenseService(balance_sheet_service)
    simplification_service = DebtSimplificationService()

    group_service = GroupService(repo, expense_service, simplification_service)

    goa_group_id = group_service.create_group("Goa Trip", [shubh, bob, tom])
    group_service.create_group("Non-Group Expenses", [shubh, bob, tom, jake])

    group_service.add_expense(
        goa_group_id,
        "Lunch Day-1",
        100,
        shubh,
        [shubh, bob],
        SplitType.EQUAL,
        None,
    )

    group_service.add_expense(
        goa_group_id,
        "Lunch Day-2",
        100,
        bob,
        [bob, tom],
        SplitType.EQUAL,
        None,
    )

    group_service.simplify_debts(goa_group_id)
    group_service.print_balances(goa_group_id)


if __name__ == "__main__":
    main()
