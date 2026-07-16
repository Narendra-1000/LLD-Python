# Designing Splitwise — LLD Q&A

**Run:** `python -m lld.splitwise.main`  
**Patterns:** Strategy · Factory · Repository · Facade · Debt simplification

---

## Q1. What problem are we solving?

**A.** Design a group expense-sharing system that:

1. Creates **groups** with members
2. Records **expenses** (one person pays, cost split among participants)
3. Supports multiple **split types** (equal, percentage)
4. Maintains **balance sheets** (who owes whom)
5. **Simplifies debts** into a minimal set of net settlements

---

## Q2. What are the core entities?

| Entity | Responsibility |
|--------|----------------|
| `User` | Frozen identity (`id`, `name`) — hashable dict key |
| `Group` | Members, expenses, per-user balance sheets |
| `Expense` | Description, amount, paid_by, splits, split_type |
| `Split` | One participant's share `(user, amount)` |
| `BalanceSheet` | `total_paid`, `total_expense`, pairwise balances |

**Balance semantics:** Positive = other owes you; Negative = you owe them.  
Invariant: `A.balances[B] == -B.balances[A]`.

---

## Q3. How is the package structured?

```
splitwise/
├── model/       # User, Group, Expense, Split, BalanceSheet
├── strategy/    # EqualSplit, PercentageSplit
├── factory/     # SplitStrategyFactory
├── repository/  # GroupRepository (ABC) + InMemory
└── service/     # GroupService, ExpenseService, BalanceSheetService,
                 # DebtSimplificationService
```

`GroupService` is the public facade; other services hide complexity.

---

## Q4. Why Strategy + Factory for splits?

**A.** Split math varies; `ExpenseService` should not care how shares are computed.

```python
strategy = SplitStrategyFactory.get_strategy(split_type)
splits = strategy.split(amount, participants, metadata)
```

| Type | Behavior |
|------|----------|
| `EQUAL` | `amount / len(participants)` |
| `PERCENTAGE` | Share by %; must sum to 100 |

New split type (EXACT, SHARES) = new strategy + factory branch — no change to `ExpenseService`.

---

## Q5. What is the add-expense flow?

```
GroupService.add_expense(...)
  → ExpenseService
      → factory → strategy.split(...)
      → create Expense, append to group
      → BalanceSheetService.update_balances(...)
           → paid_by: +total_paid
           → each participant: +total_expense
           → pairwise: debtor owes payer (skip if same person)
```

**Demo:**  
- Lunch Day-1: Shubh pays 100 for [Shubh, Bob] → Bob owes Shubh 50  
- Lunch Day-2: Bob pays 100 for [Bob, Tom] → Tom owes Bob 50  

---

## Q6. How does debt simplification work?

**A.** Greedy net settlement with heaps:

1. Compute each user's **net** (sum of pairwise balances)
2. Clear pairwise balances
3. Creditors (net > 0) and debtors (net < 0) go into heaps
4. Match largest creditor with largest debtor; settle `min(credit, |debit|)`
5. Re-push remainders until done

**After simplify on demo:** Tom pays Shubh 50 directly; Bob (intermediary) is settled.

Does **not** change totals owed — only reduces number of transactions (at most n−1 for n users).

---

## Q7. Why Repository?

**A.** `GroupRepository` ABC + `InMemoryGroupRepository` decouples storage. Swap for DB later without changing services.

---

## Q8. How do you extend this design?

| Add… | How |
|------|-----|
| EXACT / SHARES split | New `SplitStrategy` + enum + factory |
| Settlements | New service to mark debts paid |
| Multi-currency | Currency on expense + conversion before balances |
| Edit/delete expense | Reverse balance entries, then re-apply |

---

## Q9. Common interview follow-ups

**Q. Why is `User` frozen?**  
Hashable — safe as dict key in balance sheets.

**Q. Floating point on equal split of 100 among 3?**  
33.33×3 ≠ 100. Production uses cents or remainder distribution.

**Q. What if participant is not in the group?**  
`get_balance_sheet` raises `KeyError` — validation gap.

**Q. Greedy vs optimal min-cash-flow?**  
Full optimal settlement is harder (NP-hard in general graphs). Greedy on nets is practical and interview-friendly.
