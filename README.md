# Low Level Design — Python OOP

Python implementations of classic LLD interview problems. Each module is a self-contained package with models, services, strategies, and a runnable demo.

**Requirements:** Python 3.10+

## Run a module

```bash
python -m lld.<module>.main
```

| # | LLD Problem                      | Difficulty | Run Command                              | Design Q&A | Print PDF |
|---|----------------------------------|------------|------------------------------------------|------------|-----------|
| 1 | Snakes and Ladders               | Easy       | `python -m lld.snakes_and_ladder.main`   | [DESIGN.md](lld/snakes_and_ladder/DESIGN.md) | [PDF](lld/snakes_and_ladder/DESIGN.pdf) |
| 2 | Parking Lot                      | Medium     | `python -m lld.parking_lot.main`         | [DESIGN.md](lld/parking_lot/DESIGN.md) | [PDF](lld/parking_lot/DESIGN.pdf) |
| 3 | Logger                           | Medium     | `python -m lld.logger.main`              | [DESIGN.md](lld/logger/DESIGN.md) | [PDF](lld/logger/DESIGN.pdf) |
| 4 | Splitwise                        | Hard       | `python -m lld.splitwise.main`           | [DESIGN.md](lld/splitwise/DESIGN.md) | [PDF](lld/splitwise/DESIGN.pdf) |
| 5 | Doctor's Appointment             | Medium     | `python -m lld.doctors_appointment.main` | [DESIGN.md](lld/doctors_appointment/DESIGN.md) | [PDF](lld/doctors_appointment/DESIGN.pdf) |
| 6 | Car Rental System                | Medium     | `python -m lld.car_rental.main`          | [DESIGN.md](lld/car_rental/DESIGN.md) | [PDF](lld/car_rental/DESIGN.pdf) |
| 7 | ATM                              | Medium     | `python -m lld.atm.main`                 | [DESIGN.md](lld/atm/DESIGN.md) | [PDF](lld/atm/DESIGN.pdf) |
| 8 | Customer Issue Resolution System | Medium     | `python -m lld.customer_support.main`    | [DESIGN.md](lld/customer_support/DESIGN.md) | [PDF](lld/customer_support/DESIGN.pdf) |
| 9 | Rate Limiter                     | Medium     | `python -m lld.rate_limiter.main`        | [DESIGN.md](lld/rate_limiter/DESIGN.md) | [PDF](lld/rate_limiter/DESIGN.pdf) |
| — | Custom HashMap                   | Easy       | `python -m lld.hashmap.main`             | [DESIGN.md](lld/hashmap/DESIGN.md) | [PDF](lld/hashmap/DESIGN.pdf) |

Each module has a **DESIGN.md** (Q&A) and a printable **DESIGN.pdf** with:

- home study notes (how the LLD works)  
- full **DESIGN.md** content  
- full project **source code** (compact, line-numbered)  

Regenerate PDFs anytime:

```bash
.venv/bin/pip install fpdf2   # once
.venv/bin/python scripts/generate_design_pdfs.py
```

Index: [lld/ALL_LLD_DESIGN_NOTEBOOKS.pdf](lld/ALL_LLD_DESIGN_NOTEBOOKS.pdf)  
Tip: print **double-sided** to save paper.

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
