# Designing a Car Rental System — LLD Q&A

**Run:** `python -m lld.car_rental.main`  
**Patterns:** Strategy · Singleton · Factory · Repository · Thread safety

---

## Q1. What problem are we solving?

**A.** Design a multi-branch car rental system where users can:

1. Book a vehicle (**Sedan** / **SUV**) from a branch for a time window
2. Pick up at one branch and drop at another
3. Get price via a **pricing strategy** (hourly or distance-based)
4. Have a vehicle chosen via a **booking strategy** (least-booked or cheapest)
5. Pay via **payment strategy** (credit card or wallet)
6. Return the vehicle to the drop branch
7. Handle **concurrent** booking attempts safely

---

## Q2. What are the core entities?

| Entity | Responsibility |
|--------|----------------|
| `Vehicle` (Sedan, SUV) | Plate, rates, status, booking count, atomic `is_booked` |
| `Branch` | Inventory of vehicles by type |
| `Booking` | User, vehicle, pickup/drop branches, times, amount, statuses |
| `User` | Renter identity |
| `BookingService` | Singleton orchestrator for book + return |
| `AtomicBoolean` | Thread-safe compare-and-set lock on a vehicle |

---

## Q3. How is the package structured?

```
car_rental/
├── model/       # Vehicle, Branch, Booking, User, AtomicBoolean
├── service/     # BookingService, PaymentProcessor
├── strategy/    # booking/ · pricing/ · payment/
├── factory/     # VehicleFactory
├── repository/  # BranchRepository, BookingRepository
├── enums/       # VehicleType, VehicleStatus, BookingStatus, ...
└── utils/       # Date parsing, availability checker
```

---

## Q4. Why three Strategy families?

| Strategy | Question it answers |
|----------|---------------------|
| **BookingStrategy** | *Which* vehicle to pick? (least booked / cheapest) |
| **PricingStrategy** | *How much* to charge? (hourly / distance) |
| **PaymentStrategy** | *How* to pay? (card / wallet) |

Each varies independently — Open/Closed Principle without changing `BookingService` core logic.

---

## Q5. Why Singleton for `BookingService`?

**A.** One booking orchestrator shared by the app, with injected repos and strategies. Uses **double-checked locking** for thread-safe lazy init.

**Caveat:** First `get_instance(...)` locks strategies forever; later calls with different strategies are ignored.

---

## Q6. What is the booking flow?

```
BookingService.book_vehicle(branch_id, type, start, end, user, payment, ...)
  → get branch, filter AVAILABLE + not is_booked
  → booking_strategy.book_vehicle(vehicles)
       → compare_and_set(False, True)  # atomic claim
  → pricing_strategy.calculate_price(...)
  → create Booking (CREATED, PENDING)
  → PaymentProcessor.pay(...)
  → success: CONFIRMED, vehicle BOOKED, persist
  → failure: release is_booked, return None
```

---

## Q7. What is the return flow?

```
return_vehicle(booking_id)
  → booking must be CONFIRMED
  → status = COMPLETED
  → is_booked.set(False)
  → add vehicle to drop_branch inventory
```

---

## Q8. How is concurrency handled?

**A.** `AtomicBoolean.compare_and_set(False, True)` on each vehicle. Two threads booking the only SUV → exactly one wins; the other gets "No vehicle could be booked."

---

## Q9. How do you extend this design?

| Add… | How |
|------|-----|
| New vehicle type | Enum + subclass + `VehicleFactory` |
| New booking algo | Implement `BookingStrategy`, inject at init |
| New pricing | Implement `PricingStrategy` |
| New payment | Implement `PaymentStrategy`, pass per booking |
| Time-slot overlap | Wire `VehicleAvailabilityChecker` into booking |

---

## Q10. Common interview follow-ups

**Q. Is time-slot availability checked?**  
`VehicleAvailabilityChecker` exists but is **not wired** into booking. Currently one booking per vehicle via `is_booked`, not per calendar slot.

**Q. Payment vs booking/pricing injectability?**  
Payment is per-call; booking/pricing are fixed on the singleton — asymmetric by design in this demo.

**Q. `VehicleStatus.BOOKED` vs `is_booked`?**  
Two parallel flags. Return resets `is_booked` but does not set status back to `AVAILABLE` — a known simplification/gotcha.
