# Designing an ATM — LLD Q&A

**Run:** `python -m lld.atm.main`  
**Patterns:** State · Chain of Responsibility · Factory · Repository

---

## Q1. What problem are we solving?

**A.** Design an ATM cash-withdrawal machine that:

1. Accepts a **card** linked to an **account**
2. Authenticates with a **PIN**
3. Allows **withdrawal**
4. Dispenses cash using available note denominations (₹2000, ₹500, ₹100)
5. Validates ATM cash, account balance, and denomination feasibility
6. Deducts from ATM inventory and account, then ejects the card

Invalid actions in the wrong state must be rejected (e.g. withdraw before PIN).

---

## Q2. What are the core entities?

| Entity | Responsibility |
|--------|----------------|
| `ATM` | Machine id, note counts, cash available, status |
| `Card` | Card number, PIN, linked `Account` |
| `Account` | Account number, balance |
| `ATMMachine` | Context — holds current card + state; user-facing API |
| `ATMState` | Abstract state — defines valid operations |
| `CashDispenser` | CoR handler for one denomination |

---

## Q3. How is the package structured?

```
atm/
├── model/       # ATM, Card, Account
├── state/       # Idle → CardInserted → Authenticated → DispenseCash
├── cor/         # Cash dispenser chain (₹2000 → ₹500 → ₹100)
├── service/     # ATMMachine (facade/context)
├── factory/     # ATMStateFactory (status → state)
├── repository/  # In-memory ATM storage
└── enums/       # ATMStatus
```

---

## Q4. Why State Pattern?

**A.** ATM behavior depends on lifecycle stage. Each state allows only valid operations and controls transitions.

```
IDLE → CARD_INSERTED → AUTHENTICATED → DISPENSE_CASH → IDLE
```

| State | Allows |
|-------|--------|
| `IdleState` | Insert card |
| `CardInsertedState` | Enter PIN / eject |
| `AuthenticatedState` | Select option (withdraw) / eject |
| `DispenseCashState` | Dispense cash → eject → IDLE |

`ATMMachine` delegates every action to `self.state` — no giant `if status == ...` switch in one class.

---

## Q5. Why Chain of Responsibility for cash?

**A.** Each denomination handler tries to use its notes, then passes the remainder to the next:

```
₹2000 Dispenser → ₹500 Dispenser → ₹100 Dispenser
```

- `can_dispense(atm, amount)` — check if a valid combination exists  
- `dispense(atm, amount)` — deduct notes and print breakdown  

Easy to add a new denomination: new handler + wire it in `CashDispenserChainBuilder`.

---

## Q6. What is the happy-path withdrawal flow?

```
insert_card(card)     → Idle → CardInserted
enter_pin(pin)        → if correct → Authenticated
select_option("WITHDRAW") → DispenseCash
dispense_cash(amount)
  → check ATM cash ≥ amount
  → check account balance ≥ amount
  → chain.can_dispense(...)
  → chain.dispense(...)
  → deduct account + ATM cash
  → eject_card → Idle
```

---

## Q7. What are the failure paths?

| Condition | Behavior |
|-----------|----------|
| Action without card | Rejected in Idle |
| Wrong PIN | Stay in CardInserted |
| Amount > ATM cash | Eject → Idle |
| Amount > balance | Eject → Idle |
| No valid note combo | Cannot dispense → eject → Idle |

---

## Q8. Why Factory for states?

**A.** `ATMStateFactory.get_state(status, machine)` rebuilds the correct state object from a persisted `ATMStatus`. Useful after restart / crash recovery.

---

## Q9. How do you extend this design?

| Add… | How |
|------|-----|
| Deposit / balance inquiry | New states or branches in `AuthenticatedState.select_option` |
| New note (e.g. ₹50) | New `CashDispenser` + chain builder |
| PIN retry lockout | Counter in `CardInsertedState` |
| Real DB | Swap `ATMRepository` implementation |

---

## Q10. Common interview follow-ups

**Q. Why not one class with a status enum and if-else?**  
State Pattern keeps each state's rules local and open for new states without bloating one method.

**Q. Is the CoR greedy?**  
Yes — max higher notes first. It may fail when a different mix would work. Discuss DP/backtracking as an alternative.

**Q. What does `select_option` ignore?**  
In this demo it always goes to withdrawal regardless of the option string — intentional simplification.
