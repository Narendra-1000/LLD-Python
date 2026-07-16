# Designing Snakes and Ladders — LLD Q&A

**Run:** `python -m lld.snakes_and_ladder.main`  
**Patterns:** Factory · Inheritance/Polymorphism · Facade

---

## Q1. What problem are we solving?

**A.** Design a Snakes & Ladders simulator with:

1. Configurable **board size**, snakes, ladders, dice count, players
2. **Serpentine** board numbering (like a real board)
3. Random obstacle placement
4. Turn-based play with dice rolls
5. Snake/ladder effects and **exact-land-to-win** rule

---

## Q2. What are the core entities?

| Entity | Responsibility |
|--------|----------------|
| `Board` | N×N grid, serpentine numbering, obstacles, movement |
| `Cell` | Position + optional obstacle; `get_final_position()` |
| `Player` | Name + current position |
| `Dice` | Roll 1–6 per die, sum for multi-dice |
| `Obstacle` | ABC: Snake (head→tail), Ladder (bottom→top) |
| `Game` | Facade — setup, turn loop, win detection |

---

## Q3. How is the package structured?

```
snakes_and_ladder/
├── model/       # Board, Cell, Player, Dice, Obstacle, Snake, Ladder
├── factory/     # ObstacleFactory
├── service/     # Game
└── enums/       # ObstacleType
```

---

## Q4. Why Factory for obstacles?

**A.** Board placement code should not know concrete classes:

```python
ObstacleFactory.create_obstacle(ObstacleType.SNAKE, up, down)  → Snake
ObstacleFactory.create_obstacle(ObstacleType.LADDER, up, down) → Ladder
```

Board treats both uniformly via polymorphism (`move_player` / final position).

---

## Q5. How does the board layout work?

- `side_length = sqrt(size)` — size should be a perfect square  
- Cells numbered **serpentine**: row 1 L→R, row 2 R→L, etc.  
- Linear position maps to (row, col) via `_get_row` / `_get_col`

---

## Q6. What is the turn loop?

```
while more than one player in queue:
  player = players.popleft()
  roll = dice.roll()
  new_pos = board.get_new_position(player, roll)
  if overshoot (> size): stay, re-queue
  elif new_pos == size: WIN (do not re-queue)
  else: update position (apply snake/ladder), re-queue
```

Players are managed with a `deque` (round-robin).

---

## Q7. How are obstacles placed?

```
random up ∈ [2, size], down ∈ [1, up-1]
→ ObstacleFactory.create → board.add_obstacle
→ reject if src or dest cell already has an obstacle
```

---

## Q8. How do you extend this design?

| Add… | How |
|------|-----|
| Custom layouts | Load snakes/ladders from config instead of random |
| New obstacles | Teleporter/penalty extending `Obstacle` |
| Player strategies | Human input vs AI vs weighted dice |
| Exact-roll rule toggle | Config flag on overshoot behavior |

---

## Q9. Common interview follow-ups

**Q. Overshoot?**  
Player stays put and is re-queued — must land exactly on last cell to win.

**Q. Ladder constructor args?**  
`Ladder(top, bottom)` stores `src=bottom, dest=top` (args inverted vs snake).

**Q. Infinite loops?**  
Placement rejects overlapping cells; discuss validating no cycles if loading custom boards.
