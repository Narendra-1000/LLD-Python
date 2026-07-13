# Low Level Design — Python OOP

Python implementations of classic LLD interview problems. Each module is a self-contained package with models, services, strategies, and a runnable demo.

**Requirements:** Python 3.10+

## Run a module

```bash
python -m lld.<module>.main
```

| # | LLD Problem                      | Difficulty | Run Command                              | YouTube |
|---|----------------------------------|------------|------------------------------------------|---------|
| 1 | Snakes and Ladders               | Easy       | `python -m lld.snakes_and_ladder.main`   | -       |
| 2 | Parking Lot                      | Medium     | `python -m lld.parking_lot.main`         | -       |
| 3 | Logger                           | Medium     | `python -m lld.logger.main`              | -       |
| 4 | Splitwise                        | Hard       | `python -m lld.splitwise.main`           | -       |
| 5 | Doctor's Appointment             | Medium     | `python -m lld.doctors_appointment.main` | -       |
| 6 | Car Rental System                | Medium     | `python -m lld.car_rental.main`          | -       |
| 7 | ATM                              | Medium     | `python -m lld.atm.main`                 | -       |
| 8 | Customer Issue Resolution System | Medium     | `python -m lld.customer_support.main`    | -       |
| 9 | Rate Limiter                     | Medium     | `python -m lld.rate_limiter.main`        | -       |
| — | Custom HashMap                   | Easy       | `python -m lld.hashmap.main`             | —       |

## Package structure

```
lld/
├── atm/                  # State pattern + Chain of Responsibility
├── car_rental/           # Strategy + Singleton + threading
├── customer_support/     # Strategy + Repository
├── doctors_appointment/  # Strategy + Repository + waitlist
├── hashmap/              # Custom hash map data structure
├── logger/               # Singleton + Chain of Responsibility
├── parking_lot/          # Singleton + Strategy + threading
├── rate_limiter/         # Strategy + Factory + threading
├── snakes_and_ladder/    # Factory + inheritance
└── splitwise/            # Strategy + Factory + debt simplification
```
