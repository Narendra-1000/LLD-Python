# Designing a Doctor's Appointment System — LLD Q&A

**Run:** `python -m lld.doctors_appointment.main`  
**Patterns:** Strategy · Repository · DTO · FIFO waitlist

---

## Q1. What problem are we solving?

**A.** Design a doctor appointment booking system that:

1. Registers **doctors** (specialization + rating) and **patients**
2. Lets doctors declare **available time slots**
3. Lets patients **search** open slots by specialization
4. **Ranks** results via a pluggable strategy (start time or rating)
5. **Books** a slot (marks unavailable)
6. On conflict, adds patient to a **FIFO waitlist**
7. On **cancel**, frees the slot and auto-promotes the next waitlisted patient

---

## Q2. What are the core entities?

| Entity | Responsibility |
|--------|----------------|
| `Doctor` | Name, specialization, rating, `availability: dict[slot → bool]` |
| `Patient` | Name + id |
| `Booking` | patient_id, doctor_id, slot |
| `DoctorSlot` (DTO) | Transient search result: doctor + slot |
| `BookingService` | Search, book, cancel, waitlist promotion |

**Availability:** `True` = open, `False` = booked.

---

## Q3. How is the package structured?

```
doctors_appointment/
├── model/       # Doctor, Patient, Booking
├── dto/         # DoctorSlot (search result)
├── strategy/    # StartTimeRank, RatingBasedRank
├── repository/  # Doctor, Patient, Booking (+ waitlist)
├── service/     # DoctorService, PatientService, BookingService
├── exception/   # Doctor/Patient/Booking not found
├── enums/       # Specialization
└── utils/       # "12:30" → time parsing
```

---

## Q4. Why Strategy for ranking?

**A.** Search results can be sorted differently without changing search logic.

| Strategy | Sort key |
|----------|----------|
| `StartTimeRankStrategy` | Slot time ascending |
| `RatingBasedRankStrategy` | Doctor rating descending |

Strategy is passed **at call time** (not constructor) so the same session can rank by time then by rating.

```python
booking_service.search(Specialization.CARDIOLOGIST, StartTimeRankStrategy())
```

No factory here — caller chooses explicitly.

---

## Q5. What is the book + waitlist + cancel flow?

```
book(patient, doctor, "12:30")
  → if slot open: create Booking, mark False, done
  → if taken: add_to_waitlist("{doctor_id}-{slot}"), raise error

cancel(booking_id)
  → mark slot True, delete booking
  → pop_from_waitlist(...)
  → if next patient: book(next, doctor, slot)  # auto-promote
```

**Demo:** Shubh books Curious @ 12:30 → Kunal waitlisted → Shubh cancels → Kunal auto-booked.

Waitlist uses `collections.deque` (FIFO) keyed by `"{doctor_id}-{slot}"`.

---

## Q6. Why a DTO (`DoctorSlot`)?

**A.** Search returns a composite of doctor + slot that is **never persisted**. `Booking` is the persisted record. Keeps query shape separate from storage.

---

## Q7. Why three services?

| Service | Owns |
|---------|------|
| `DoctorService` | Register + declare availability |
| `PatientService` | Register + lookup |
| `BookingService` | Search / book / cancel — orchestrates all repos |

Avoids one god-class service.

---

## Q8. How do you extend this design?

| Add… | How |
|------|-----|
| New ranking (fee, distance) | Implement `SlotRankStrategy` |
| Date-aware slots | Replace `str` slot with date+time value object |
| Concurrency | Lock per doctor-slot or DB unique constraint |
| Better errors | Replace `RuntimeError` with domain exceptions |
| Single source of truth | Derive availability from bookings only |

---

## Q9. Common interview follow-ups

**Q. Dual source of truth?**  
`Doctor.availability` + `BookingRepository` both track booked state. Could derive open slots from declared slots minus bookings.

**Q. Patient conflict check?**  
Only same slot **string** across bookings — patient could book `"12:30"` with two doctors (no date).

**Q. Slots have no date?**  
`"12:30"` Monday vs Tuesday are indistinguishable — intentional demo limit.

**Q. Strategy at call time vs constructor?**  
Call-time is more flexible when ranking preference changes per search.
