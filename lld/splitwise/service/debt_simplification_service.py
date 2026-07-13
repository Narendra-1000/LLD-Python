import heapq
from typing import Dict, List

from ..model.group import Group
from ..model.user import User


class _CreditorEntry:
    def __init__(self, user: User, net: float) -> None:
        self.user = user
        self.net = net

    def __lt__(self, other: "_CreditorEntry") -> bool:
        return self.net > other.net


class _DebtorEntry:
    def __init__(self, user: User, net: float) -> None:
        self.user = user
        self.net = net

    def __lt__(self, other: "_DebtorEntry") -> bool:
        return self.net < other.net


class DebtSimplificationService:
    def simplify_debts(self, group: Group) -> None:
        users: List[User] = list(group.members)
        sheets = group.balance_sheets

        net_balances: Dict[User, float] = {}
        for user in users:
            net = 0.0
            balances = sheets[user].balances
            for amount in balances.values():
                net += amount
            net_balances[user] = net
            sheets[user].clear_balances()

        creditors: List[_CreditorEntry] = []
        debtors: List[_DebtorEntry] = []

        for user in users:
            net = net_balances[user]
            if net > 0:
                heapq.heappush(creditors, _CreditorEntry(user, net))
            elif net < 0:
                heapq.heappush(debtors, _DebtorEntry(user, net))

        while creditors and debtors:
            creditor_entry = heapq.heappop(creditors)
            debtor_entry = heapq.heappop(debtors)
            creditor = creditor_entry.user
            debtor = debtor_entry.user

            credit_amount = net_balances[creditor]
            debit_amount = net_balances[debtor]

            settled_amount = min(credit_amount, -debit_amount)

            sheets[creditor].add_balance(debtor, settled_amount)
            sheets[debtor].add_balance(creditor, -settled_amount)

            net_balances[creditor] = credit_amount - settled_amount
            net_balances[debtor] = debit_amount + settled_amount

            if net_balances[creditor] > 0:
                heapq.heappush(
                    creditors, _CreditorEntry(creditor, net_balances[creditor])
                )
            if net_balances[debtor] < 0:
                heapq.heappush(
                    debtors, _DebtorEntry(debtor, net_balances[debtor])
                )
