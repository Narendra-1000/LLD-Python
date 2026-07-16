# Designing a Customer Issue Resolution System — LLD Q&A

**Run:** `python -m lld.customer_support.main`  
**Patterns:** Strategy · Repository · Service layer

---

## Q1. What problem are we solving?

**A.** Design a fintech customer support system that:

1. Lets customers create **issues** (tickets) tied to transactions
2. Registers **agents** with domain **expertise**
3. **Assigns** issues to available matching agents
4. Supports issue lifecycle: OPEN → IN_PROGRESS → RESOLVED / WAITING
5. Filters issues and tracks agent work history
6. Waitlists issues when no free agent matches

---

## Q2. What are the core entities?

| Entity | Responsibility |
|--------|----------------|
| `Issue` | Ticket id, type, status, resolution, assigned agent |
| `Agent` | Expertise set, current assignment, waitlist (`deque`), history |
| `IssueService` | Create, filter, update, resolve |
| `AgentService` | Register agents, view history |
| `AssignmentService` | Delegates to assignment strategy; waitlist fallback |

---

## Q3. How is the package structured?

```
customer_support/
├── model/       # Issue, Agent
├── repository/  # IssueRepository, AgentRepository
├── service/     # IssueService, AgentService, AssignmentService
├── strategy/    # AssignmentStrategy + DefaultAssignmentStrategy
└── enums/       # IssueStatus, IssueType
```

---

## Q4. Why Strategy for assignment?

**A.** How we pick an agent can change without touching `AssignmentService`.

```python
class AssignmentStrategy(ABC):
    def assign(self, agents, issue) -> Optional[Agent]: ...
```

**Default:** first available agent whose expertise contains the issue type.

Easy to add: RoundRobin, LeastLoaded, SkillWeighted.

---

## Q5. What are the main flows?

**Create issue**
```
IssueService.create_issue(...) → Issue(OPEN) → save
```

**Assign**
```
AssignmentService.assign_issue(id)
  → strategy.assign(agents, issue)
  → found: link agent ↔ issue
  → else: add to waitlist of matching agents, status WAITING
```

**Resolve**
```
IssueService.resolve_issue(id, resolution)
  → RESOLVED + resolution
  → append to agent history, free agent
```

---

## Q6. Why Repository?

**A.** Services talk to `IssueRepository` / `AgentRepository` (in-memory dicts). Swap for DB/Redis later without changing business logic.

---

## Q7. How do you extend this design?

| Add… | How |
|------|-----|
| New assignment algo | Implement `AssignmentStrategy` |
| New issue type | Add to `IssueType` enum |
| Auto-drain waitlist | On resolve, pop next waitlisted issue for that agent |
| Notifications | Observer on status changes |

---

## Q8. Common interview follow-ups

**Q. Waitlist behavior?**  
Same issue can be added to **all** matching agents' waitlists — not a single shared queue. Discuss draining on free-agent as a follow-up.

**Q. How does filtering work?**  
`get_issues(filters)` — e.g. by email or type; type string normalizes spaces to underscores for enum match.

**Q. Double assignment?**  
Guarded by `agent.is_available()` only — no distributed lock in this demo.
