# Designing a Parking Lot — LLD Q&A

**Run:** `python -m lld.parking_lot.main`  
**Patterns:** Singleton · Strategy · Factory · Thread safety

---

## Q1. What problem are we solving?

**A.** Design a multi-floor parking lot that:

1. Accepts vehicles (Bike / Car / Truck) at an **entry gate**
2. Finds a matching free spot and issues a **ticket**
3. On exit, calculates a **fee** using a pricing strategy
4. Accepts **payment** (Cash / UPI / Card)
5. Vacates the spot only after successful payment

Also handle **concurrent** park attempts safely so two vehicles cannot claim the same spot.

---

## Q2. What are the core entities?

| Entity | Responsibility |
|--------|----------------|
| `Vehicle` (Car, Bike, Truck) | Vehicle number + type |
| `ParkingSpot` | One spot for one vehicle type; thread-safe occupy/vacate |
| `ParkingFloor` | Collection of spots; finds first free matching spot |
| `Ticket` | Session: ticket id, entry time, vehicle, floor, spot, payment status |
| `EntryGate` / `ExitGate` | Thin facades over `ParkingLot` |
| `ParkingLot` | Singleton orchestrator — floors, active tickets, pricing |

---

## Q3. How is the package structured?

```
parking_lot/
├── model/       # Domain entities (Vehicle, Spot, Floor, Ticket, Gate)
├── service/     # ParkingLot, PaymentProcessor
├── strategy/    # Pricing + Payment algorithms
├── factory/     # Vehicle / Pricing / Payment creation
├── enums/       # VehicleType, PaymentMode, PricingStrategyType, ...
└── utils/       # Date-time parsing
```

| Layer | Why it exists |
|-------|----------------|
| **model** | Pure domain objects — little business logic |
| **service** | Orchestration and state |
| **strategy** | Swappable fee & payment algorithms (OCP) |
| **factory** | Enum → concrete class without `if/else` in callers |
| **enums** | Type-safe constants |

---

## Q4. Why Singleton for `ParkingLot`?

**A.** There is one physical lot. All entry/exit gates must share the same floors, spots, and active tickets.

```python
ParkingLot.get_instance()  # shared by EntryGate and ExitGate
```

Gates call `ParkingLot.get_instance()` instead of holding separate lot instances.

---

## Q5. Why Strategy for pricing and payment?

**A.** Fee rules and payment channels change independently. Strategy lets us add new algorithms without changing `ParkingLot`.

- **Pricing:** `TimeBasedPricing` (peak/off-peak hourly) vs `EventBasedPricing` (flat hourly)
- **Payment:** `CashPayment`, `CardPayment`, `UpiPayment`

`ParkingLot` only depends on the interface:

```python
fee = self.pricing_strategy.calculate_fee(vehicle_type, entry_time, exit_time)
```

---

## Q6. Why Factory?

**A.** Callers pass an enum (`VehicleType.CAR`, `PaymentMode.UPI`) instead of constructing concrete classes. Creation logic stays in one place.

| Factory | Maps |
|---------|------|
| `VehicleFactory` | `VehicleType` → Car / Bike / Truck |
| `PricingStrategyFactory` | `PricingStrategyType` → Time / Event based |
| `PaymentStrategyFactory` | `PaymentMode` → Cash / UPI / Card |

---

## Q7. What is the entry (park) flow?

```
EntryGate.park_vehicle(vehicle, entry_time)
  → ParkingLot.park_vehicle(...)
      → for each floor: find_available_spot(vehicle.type)
           → ParkingSpot.try_occupy()   # locked
      → create Ticket (UUID), store in active_tickets
      → return Ticket (or None if full)
```

**Spot rule:** Exact type match only (Car cannot use Truck spot).  
**Allocation:** First-fit across floors.

---

## Q8. What is the exit (unpark) flow?

```
ExitGate.unpark_vehicle(ticket_id, exit_time, payment_mode)
  → lookup ticket
  → pricing_strategy.calculate_fee(...)
  → PaymentStrategyFactory.get(mode) → PaymentProcessor.pay(...)
  → on success: vacate spot, remove ticket
  → on failure: abort — spot stays occupied
```

---

## Q9. How is concurrency handled?

**A.** Each `ParkingSpot` has a `threading.Lock`. `try_occupy()` atomically claims the spot:

```python
def try_occupy(self) -> bool:
    with self._lock:
        if not self._occupied:
            self._occupied = True
            return True
        return False
```

`main.py` parks two bikes on two threads to demonstrate this. With one bike spot, only one succeeds.

---

## Q10. TIME_BASED vs EVENT_BASED pricing?

| | Time-based | Event-based |
|---|------------|-------------|
| Logic | Hour-by-hour peak (8 AM–5 PM) vs non-peak | Flat rate per hour |
| Bike | Peak ₹15 / Non-peak ₹10 | ₹30/hr |
| Car | Peak ₹30 / Non-peak ₹20 | ₹50/hr |
| Truck | Peak ₹50 / Non-peak ₹30 | ₹70/hr |

Default in `ParkingLot` is TIME_BASED; the demo switches to EVENT_BASED.

---

## Q11. How do you extend this design?

| Add… | Steps |
|------|--------|
| New vehicle (e.g. EV) | Enum + model class + factory branch + rates + spots |
| New pricing | Implement `PricingStrategy` + factory + enum |
| New payment | Implement `PaymentStrategy` + factory + enum |

`ParkingLot.unpark_vehicle` does not need changes — it already depends on interfaces.

---

## Q12. Common interview follow-ups

**Q. What if payment fails?**  
Spot stays occupied; ticket remains in `active_tickets`.

**Q. Where is ticket linked to spot?**  
`Ticket` stores `floor_id` + `spot_id`; exit looks them up to vacate.

**Q. What's not modeled?**  
Reservations, handicap/EV charging, size hierarchy (Car in Truck spot), persistent storage, receipt entity.

**Q. Is the Singleton thread-safe?**  
Lazy init without a lock — fine for demo; production would use a lock or module-level instance.
