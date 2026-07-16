#!/usr/bin/env python3
"""Generate human-readable LLD study-note PDFs (home notes style)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
LLD = ROOT / "lld"
FONT = "/Library/Fonts/Arial Unicode.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

BOX_FILL = (232, 240, 254)
BOX_BORDER = (60, 100, 160)
STEP_FILL = (255, 248, 230)
NOTE_FILL = (236, 253, 245)
WARN_FILL = (254, 243, 242)


def safe(text: str) -> str:
    # Keep readable ASCII for PDF fonts; map common unicode from notes/code
    repl = {
        "—": "-", "–": "-", "→": "->", "←": "<-", "•": "-", "×": "x",
        "₹": "Rs.", "«": "<<", "»": ">>", "≥": ">=", "≤": "<=", "≠": "!=",
        "├": "|", "└": "|", "─": "-", "│": "|", "┌": "+", "┐": "+",
        "┘": "+", "┬": "+", "┴": "+", "┼": "+", "═": "=", "║": "|",
        "✓": "OK", "✗": "X", "…": "...", "\u00a0": " ",
    }
    for a, b in repl.items():
        text = text.replace(a, b)
    # Drop any remaining non-encodable oddities for the font
    return "".join(ch if ord(ch) < 0x10000 else "?" for ch in text)


@dataclass
class Box:
    title: str
    lines: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Home-note content per project (plain language)
# ---------------------------------------------------------------------------

PROJECTS: dict[str, dict] = {
    "parking_lot": {
        "title": "Parking Lot - How it works",
        "one_liner": "Car comes in -> find a free spot -> give ticket -> on exit charge money -> free the spot.",
        "story": (
            "Imagine a mall parking. You drive to the entry gate. The system looks for a free spot "
            "that matches your vehicle (bike spot for bike, car spot for car). If it finds one, "
            "it locks that spot and prints a ticket. When you leave, it looks at how long you stayed, "
            "calculates the fee, takes payment, then unlocks the spot for the next person."
        ),
        "cast": [
            ("ParkingLot", "The brain. Remembers all floors, spots, and active tickets. Only ONE exists (Singleton)."),
            ("EntryGate / ExitGate", "The doors. They don't do heavy work - they just call ParkingLot."),
            ("ParkingFloor", "One floor of the building. Holds many ParkingSpots."),
            ("ParkingSpot", "One parking place. Has a lock so two cars cannot grab it at the same time."),
            ("Vehicle (Car/Bike/Truck)", "What is parking. Type decides which spot is allowed."),
            ("Ticket", "Your receipt for this visit: which floor, which spot, entry time."),
            ("PricingStrategy", "How to calculate money (peak hours vs flat event rate). Easy to swap."),
            ("PaymentStrategy", "How you pay (cash / card / UPI). Easy to swap."),
        ],
        "walkthrough": [
            "You arrive with a Bike at EntryGate.",
            "EntryGate asks ParkingLot: park this bike.",
            "ParkingLot checks Floor 1 spots. Finds a BIKE spot that is free.",
            "Spot.tryOccupy() locks it (thread-safe). Nobody else can take it.",
            "A Ticket is created (ticket id + entry time + spot id) and saved in activeTickets.",
            "Later at ExitGate you give ticket id + choose UPI.",
            "ParkingLot asks PricingStrategy: how much for this bike from entry to now?",
            "PaymentStrategy (UPI) processes payment. If OK, spot is vacated and ticket removed.",
            "If payment fails, spot stays occupied - you did not leave yet.",
        ],
        "why_patterns": [
            ("Why Singleton?", "There is one physical parking lot. All gates must share the same spots and tickets."),
            ("Why Strategy for price/pay?", "Tomorrow mall may change rates or add Wallet pay. Add a new class - don't rewrite ParkingLot."),
            ("Why Factory?", "Pass VehicleType.CAR instead of writing if/else everywhere to create Car/Bike/Truck."),
            ("Why lock on Spot?", "Two threads (two bikes) might race for the last spot. Lock makes only one win."),
        ],
        "boxes": [
            Box("ParkingLot (brain)", ["floors", "activeTickets", "pricingStrategy", "park / unpark"]),
            Box("ParkingFloor", ["spots list", "find free spot"]),
            Box("ParkingSpot", ["type allowed", "occupied?", "tryOccupy / vacate"]),
            Box("Ticket", ["id, time", "vehicle", "floor + spot"]),
        ],
        "remember": [
            "Spot type must match vehicle type (car cannot use truck spot in this design).",
            "Ticket stores floor_id + spot_id so exit knows what to free.",
            "Payment failure = no unpark.",
            "Demo main.py parks two bikes concurrently to show the lock.",
        ],
        "oops_simple": [
            ("Encapsulation", "Spot hides occupied flag. Outside world only calls tryOccupy/vacate."),
            ("Abstraction", "PricingStrategy only says calculateFee - not how peak hours work."),
            ("Inheritance", "Car, Bike, Truck are kinds of Vehicle."),
            ("Polymorphism", "ParkingLot calls calculateFee without caring if it is TimeBased or EventBased."),
        ],
    },
    "atm": {
        "title": "ATM - How it works",
        "one_liner": "Insert card -> PIN -> withdraw -> machine gives notes -> card comes out.",
        "story": (
            "An ATM is like a vending machine for cash, but it must follow steps in order. "
            "You cannot withdraw before entering PIN. You cannot insert two cards at once. "
            "So we model the machine as states: Idle, Card Inserted, Authenticated, Dispense Cash. "
            "Giving notes is a chain: try Rs.2000 notes first, then Rs.500, then Rs.100."
        ),
        "cast": [
            ("ATMMachine", "The face of the ATM. You talk to it; it forwards work to the current state."),
            ("IdleState", "No card. Only insertCard is allowed."),
            ("CardInsertedState", "Waiting for PIN. Wrong PIN? Stay here. Right PIN? Move to Authenticated."),
            ("AuthenticatedState", "Logged in. Choose withdraw (demo)."),
            ("DispenseCashState", "Check balances, run note chain, give cash, eject card, back to Idle."),
            ("CashDispenser chain", "2000 handler -> 500 handler -> 100 handler. Each takes what it can, passes rest."),
            ("Card / Account", "Card has PIN; Account has balance."),
        ],
        "walkthrough": [
            "Machine starts in Idle.",
            "insertCard(card) -> now CardInserted.",
            "enterPin: if wrong, stay; if correct -> Authenticated.",
            "selectOption(WITHDRAW) -> DispenseCash.",
            "dispenseCash(amount): check ATM has enough cash, account has enough balance.",
            "Chain asks: can we make this amount with available notes?",
            "If yes, notes are deducted, account balance reduced, card ejected -> Idle.",
            "If no, message shown, card ejected -> Idle (no money given).",
        ],
        "why_patterns": [
            ("Why State?", "Each step allows different actions. Avoids one giant if status==... mess."),
            ("Why Chain of Responsibility?", "Each denomination is one small class. Add Rs.50 later by adding one handler."),
            ("Why Factory for state?", "If ATM restarts mid-session, rebuild the right state from saved status."),
        ],
        "boxes": [
            Box("ATMMachine", ["current state", "current card", "insert/pin/withdraw"]),
            Box("States", ["Idle", "CardInserted", "Authenticated", "DispenseCash"]),
            Box("Dispenser chain", ["2000 -> 500 -> 100", "canDispense / dispense"]),
            Box("Account", ["balance", "deduct on success"]),
        ],
        "remember": [
            "Wrong step in wrong state is rejected (e.g. withdraw while Idle).",
            "Dispensing is greedy (max big notes first) - interview follow-up topic.",
            "Demo option string is mostly ignored - always goes to withdraw.",
        ],
        "oops_simple": [
            ("Encapsulation", "Only the current state decides what is allowed."),
            ("Abstraction", "ATMState defines the buttons; each state implements them differently."),
            ("Inheritance", "IdleState etc. are ATMStates; note classes are CashDispensers."),
            ("Polymorphism", "machine.insertCard() calls whatever state is current."),
        ],
    },
    "car_rental": {
        "title": "Car Rental - How it works",
        "one_liner": "Pick branch + car type -> system chooses a free car -> price it -> pay -> later return at drop branch.",
        "story": (
            "You want an SUV from Branch B1 for the weekend. The system filters free SUVs, "
            "then a booking strategy picks which one (least used, or cheapest). Price can be "
            "by hours or by km. Payment can be card or wallet. Two people booking the last SUV "
            "at the same time? AtomicBoolean makes sure only one wins."
        ),
        "cast": [
            ("BookingService", "Main coordinator (Singleton). bookVehicle / returnVehicle."),
            ("Branch", "A location that holds vehicles."),
            ("Vehicle (Sedan/SUV)", "The car. Has price, status, and a tiny lock flag isBooked."),
            ("BookingStrategy", "Which car to pick from the free list."),
            ("PricingStrategy", "How much to charge."),
            ("PaymentStrategy", "How customer pays."),
            ("Booking", "The order record linking user, car, times, branches, money."),
            ("AtomicBoolean", "compareAndSet(False, True) = claim the car safely under concurrency."),
        ],
        "walkthrough": [
            "bookVehicle(branch, SUV, start, end, user, payment)...",
            "Load branch inventory; keep only AVAILABLE and not already flagged booked.",
            "BookingStrategy tries cars; first successful compareAndSet wins the car.",
            "PricingStrategy calculates amount for the time/distance.",
            "Create Booking (CREATED). Try payment.",
            "Payment OK -> CONFIRMED, car status BOOKED, save booking.",
            "Payment fail -> release isBooked flag so someone else can take the car.",
            "returnVehicle: mark COMPLETED, clear isBooked, add car to drop branch.",
        ],
        "why_patterns": [
            ("Why 3 Strategies?", "Choosing a car, pricing, and paying change for different business rules - separately."),
            ("Why Singleton service?", "One booking desk for the app (demo). Note: first init locks strategies."),
            ("Why AtomicBoolean?", "Same idea as parking spot lock - race for last car."),
        ],
        "boxes": [
            Box("BookingService", ["strategies", "repos", "book / return"]),
            Box("Branch", ["vehicles by type"]),
            Box("Vehicle + lock", ["isBooked CAS", "bookingCount"]),
            Box("Booking", ["user, car", "money, status"]),
        ],
        "remember": [
            "Time-slot overlap checker exists in utils but is NOT wired - currently one booking per car via flag.",
            "Payment strategy is passed per booking call; booking/pricing strategies are fixed on singleton.",
            "Demo: two threads fight for one SUV - only one booking succeeds.",
        ],
        "oops_simple": [
            ("Encapsulation", "Lock flag hidden inside AtomicBoolean."),
            ("Abstraction", "Strategies only expose one method each."),
            ("Inheritance", "Sedan/SUV extend Vehicle."),
            ("Polymorphism", "Service calls bookVehicle/calculatePrice without knowing concrete strategy."),
        ],
    },
    "splitwise": {
        "title": "Splitwise - How it works",
        "one_liner": "Friends share expenses -> system tracks who owes whom -> simplify into fewer payments.",
        "story": (
            "Goa trip: Shubh pays 100 for lunch with Bob (equal) -> Bob owes Shubh 50. "
            "Next day Bob pays 100 for lunch with Tom -> Tom owes Bob 50. "
            "Instead of Bob collecting from Tom and paying Shubh, simplify: Tom pays Shubh 50 directly. "
            "Bob is settled as the middle person."
        ),
        "cast": [
            ("Group", "A trip or circle. Holds members, expenses, and each person's BalanceSheet."),
            ("User", "A friend (frozen id+name - can be dict key)."),
            ("Expense", "One bill: who paid, how much, how it was split."),
            ("Split", "One person's share of that bill."),
            ("BalanceSheet", "For one user: total paid, total spent, and map of 'I owe X / X owes me'."),
            ("SplitStrategy", "Equal or Percentage math."),
            ("GroupService", "Simple API you call from outside (facade)."),
            ("DebtSimplificationService", "Uses heaps to reduce pairwise debts to net settlements."),
        ],
        "walkthrough": [
            "createGroup('Goa Trip', [Shubh, Bob, Tom]) - each gets empty BalanceSheet.",
            "addExpense Lunch1: Shubh paid 100, split equal [Shubh, Bob].",
            "Balance update: Bob owes Shubh 50 (and reverse +50 on Shubh's sheet).",
            "addExpense Lunch2: Bob paid 100, split equal [Bob, Tom] -> Tom owes Bob 50.",
            "simplifyDebts: compute net per person, clear pairwise, match biggest creditor with biggest debtor.",
            "Result: Tom -> Shubh 50. Bob net zero.",
            "printBalances shows the friendly summary.",
        ],
        "why_patterns": [
            ("Why Strategy + Factory for splits?", "Equal today, percentage tomorrow - same addExpense path."),
            ("Why Facade GroupService?", "Caller shouldn't wire ExpenseService + BalanceSheet + Simplifier manually."),
            ("Why simplify?", "Fewer UPI transfers between friends. Totals stay fair; paths get shorter."),
        ],
        "boxes": [
            Box("Group", ["members", "expenses", "balanceSheets"]),
            Box("Expense + Splits", ["paidBy", "shares"]),
            Box("BalanceSheet", ["owes map", "total paid/spent"]),
            Box("Simplifier", ["nets + heaps", "fewer payments"]),
        ],
        "remember": [
            "Invariant: if A shows +50 for B, B shows -50 for A.",
            "Payer who is also participant still gets expense share but no self-debt row.",
            "Floating point (100/3) is a real interview gotcha - use cents in production.",
            "Participant not in group -> KeyError (validation gap).",
        ],
        "oops_simple": [
            ("Encapsulation", "You update balances through service methods, not raw dicts from outside."),
            ("Abstraction", "SplitStrategy hides equal vs percentage math."),
            ("Inheritance", "EqualSplit / PercentageSplit implement the same interface."),
            ("Polymorphism", "factory returns a strategy; expense code just calls split()."),
        ],
    },
    "doctors_appointment": {
        "title": "Doctor Appointment - How it works",
        "one_liner": "Doctor opens slots -> patient searches -> books -> if taken, waitlist -> cancel promotes next patient.",
        "story": (
            "Doctor Curious (cardiologist) opens 9:30, 12:30, 16:00. Shubh books 12:30. "
            "Kunal tries the same slot and gets waitlisted. Shubh cancels - Kunal is auto-booked. "
            "Search can sort slots by start time or by doctor rating (strategy)."
        ),
        "cast": [
            ("Doctor", "Has specialization, rating, and availability map: slot -> free/busy."),
            ("Patient", "Person booking."),
            ("Booking", "Links patient + doctor + slot."),
            ("BookingService", "search, book, cancel, waitlist promotion."),
            ("DoctorSlot (DTO)", "Temporary search result (doctor + slot) - not saved as its own table row."),
            ("SlotRankStrategy", "Sort search results (by time or by rating)."),
            ("Waitlist", "FIFO queue per doctor-slot key inside BookingRepository."),
        ],
        "walkthrough": [
            "Doctor registers and declareAvailability(['9:30','12:30',...]).",
            "Patient searches CARDIOLOGIST with StartTimeRankStrategy - sees free slots sorted.",
            "Shubh book(Curious, 12:30): slot free -> create Booking, mark availability False.",
            "Kunal book same slot: already False -> add Kunal to waitlist, raise error message.",
            "Shubh cancel: mark slot True, delete booking, pop waitlist -> book(Kunal) automatically.",
            "Kunal now has the 12:30 booking.",
        ],
        "why_patterns": [
            ("Why Strategy on search?", "Same list of slots, different sort - by time vs rating - without rewriting search."),
            ("Why waitlist queue?", "Fair order: first waiting patient gets the slot when it frees."),
            ("Why DTO DoctorSlot?", "Search needs doctor+slot together; we don't want to fake-save that pair."),
        ],
        "boxes": [
            Box("Doctor", ["spec, rating", "availability map"]),
            Box("BookingService", ["search / book / cancel"]),
            Box("Waitlist deque", ["per doctor-slot", "FIFO promote"]),
            Box("Rank strategy", ["by time", "by rating"]),
        ],
        "remember": [
            "Slots are strings like '12:30' - no date in this demo (Mon vs Tue look the same).",
            "Booked slots disappear from search (only free ones shown).",
            "Re-declare availability on a booked slot could wrongly mark it free - careful.",
        ],
        "oops_simple": [
            ("Encapsulation", "Waitlist lives inside repository; services use add/pop helpers."),
            ("Abstraction", "rank(slots) hides sorting details."),
            ("Inheritance", "StartTime and Rating strategies share one interface."),
            ("Polymorphism", "search calls strategy.rank without knowing which sort."),
        ],
    },
    "customer_support": {
        "title": "Customer Support - How it works",
        "one_liner": "Customer raises issue -> assign to free agent with right skill -> agent resolves -> history saved.",
        "story": (
            "Think of a fintech helpdesk. Issues have types (payment, gold, etc.). Agents have expertise. "
            "Assignment strategy picks the first free agent who knows that type. If nobody free, "
            "issue goes to waitlists. Resolve frees the agent and stores the issue in their history."
        ),
        "cast": [
            ("Issue", "The ticket (type, status, customer email, resolution)."),
            ("Agent", "Person with expertise set, optional current issue, waitlist, history."),
            ("IssueService", "Create, filter, update, resolve issues."),
            ("AssignmentService", "Asks strategy for an agent; else waitlist."),
            ("AssignmentStrategy", "Default: first available + expertise match."),
            ("AgentService", "Register agents and view work history."),
        ],
        "walkthrough": [
            "createIssue(...) -> status OPEN, saved.",
            "assignIssue(id) -> strategy scans agents.",
            "Found free expert -> link agent <-> issue, mark work in progress style flow.",
            "No free agent -> issue WAITING, pushed to waitlists of matching agents.",
            "resolveIssue(id, text) -> RESOLVED, clear agent assignment, append to history.",
        ],
        "why_patterns": [
            ("Why Strategy?", "Today first-match; tomorrow round-robin or least-loaded - swap class only."),
            ("Why separate services?", "Creating tickets vs assigning vs agent admin stay readable."),
        ],
        "boxes": [
            Box("Issue", ["type, status", "assigned agent?"]),
            Box("Agent", ["expertise", "busy?", "waitlist", "history"]),
            Box("Assignment", ["strategy picks", "or waitlist"]),
            Box("Resolve", ["free agent", "save history"]),
        ],
        "remember": [
            "Same waiting issue may be added to ALL matching agents' waitlists (demo behavior).",
            "Waitlist is not auto-drained on resolve in this code - good improvement exercise.",
        ],
        "oops_simple": [
            ("Encapsulation", "Repos hide storage dictionaries."),
            ("Abstraction", "assign(agents, issue) is the only assignment contract."),
            ("Inheritance", "DefaultAssignmentStrategy implements AssignmentStrategy."),
            ("Polymorphism", "AssignmentService calls strategy.assign blindly."),
        ],
    },
    "logger": {
        "title": "Logger - How it works",
        "one_liner": "You call logger.error('msg') -> message walks a chain of level handlers -> subscribed outputs print/write it.",
        "story": (
            "Like Log4j in miniature. Logger is global (Singleton). Handlers form a chain: "
            "Debug -> Info -> Warn -> Error -> Fatal. When Error matches, it notifies appenders "
            "(console, file). Each appender formats the text (plain or JSON) then writes."
        ),
        "cast": [
            ("Logger", "Your API: info(), error(), ... Builds LogMessage and starts the chain."),
            ("LogHandler chain", "Each handler checks 'is this my level?' else pass to next."),
            ("LogAppender", "Where it goes: console or file."),
            ("LogFormatter", "How it looks: plain text or JSON-like."),
            ("LogMessage", "level + text + timestamp."),
        ],
        "walkthrough": [
            "logger.error('disk full') creates LogMessage(ERROR, ...).",
            "DebugHandler: not my level -> pass.",
            "InfoHandler, WarnHandler: pass.",
            "ErrorHandler: match! notify all subscribed appenders.",
            "ConsoleAppender formats and prints; FileAppender locks and appends to file.",
            "Done. Fatal would travel one step further if level were FATAL.",
        ],
        "why_patterns": [
            ("Why chain?", "Different levels can have different outputs (info only console, error also file)."),
            ("Why Observer (subscribe)?", "Add a new destination without changing Logger."),
            ("Why Strategy formatter?", "Same file appender can switch plain vs JSON."),
        ],
        "boxes": [
            Box("Logger", ["getInstance", "info/error/..."]),
            Box("Handler chain", ["Debug->...->Fatal", "exact level match"]),
            Box("Appenders", ["Console", "File + lock"]),
            Box("Formatter", ["Plain", "JSON-ish"]),
        ],
        "remember": [
            "This demo matches EXACT level, not 'Error and above'.",
            "TRACE exists in enum but is not wired in the chain.",
            "File appender uses a lock for concurrent writes.",
        ],
        "oops_simple": [
            ("Encapsulation", "Callers never touch the chain - only Logger methods."),
            ("Abstraction", "append(message) / format(message) hide destinations."),
            ("Inheritance", "Each level has its handler class."),
            ("Polymorphism", "handle() behaves differently per handler."),
        ],
    },
    "rate_limiter": {
        "title": "Rate Limiter - How it works",
        "one_liner": "Before handling an API call, ask: has this user used too many requests? Allow or block.",
        "story": (
            "FREE users get a Token Bucket (burst-friendly, ~10 per minute in demo). "
            "PREMIUM users get a Fixed Window (100 per minute). "
            "Service picks the limiter by tier. Under the hood each algorithm keeps per-user state with a Lock."
        ),
        "cast": [
            ("RateLimiterService", "Public door: allowRequest(user) -> True/False."),
            ("TokenBucket", "Tokens refill over time. Empty bucket = blocked. Allows short bursts."),
            ("FixedWindow", "Count requests in the current time window; reset when window id changes."),
            ("SlidingWindowLog", "Remember timestamps; drop old ones; count what's inside the window."),
            ("RateLimiterFactory", "Build the right algorithm from an enum + config."),
            ("User + tier", "Who is calling and which plan they are on."),
        ],
        "walkthrough": [
            "API receives request for user U.",
            "Service looks at U.tier -> picks limiter.",
            "Limiter.allowRequest(U.id) under lock.",
            "Algorithm says yes -> process API. No -> return 429-style block.",
            "main.py fires 20 threads at once on FREE tier - only ~10 pass token bucket.",
        ],
        "why_patterns": [
            ("Why Strategy?", "Same allowRequest API, different math per plan."),
            ("Why Factory?", "Create limiters without scattering if/else in the service."),
            ("Why Lock?", "Counters/tokens must not corrupt under concurrent requests."),
        ],
        "boxes": [
            Box("Service", ["tier -> limiter", "allowRequest"]),
            Box("Token Bucket", ["refill", "burst OK"]),
            Box("Fixed Window", ["count / window", "edge burst risk"]),
            Box("Sliding Log", ["timestamp list", "smoother"]),
        ],
        "remember": [
            "Fixed window can burst at boundaries (end of W1 + start of W2).",
            "In-memory only - multi-server needs Redis for shared limits.",
            "Some enum algos are listed but not implemented yet - good practice task.",
        ],
        "oops_simple": [
            ("Encapsulation", "Token maps stay private inside the limiter."),
            ("Abstraction", "Caller only knows allowRequest."),
            ("Inheritance", "Each algorithm extends RateLimiter."),
            ("Polymorphism", "Service calls allowRequest on whatever algorithm tier mapped to."),
        ],
    },
    "snakes_and_ladder": {
        "title": "Snakes & Ladders - How it works",
        "one_liner": "Players take turns rolling dice, move on a serpentine board, snakes send you down, ladders up, exact land to win.",
        "story": (
            "Game builds an N x N board (size should be a perfect square). Snakes and ladders are "
            "placed randomly via a factory. Players sit in a queue. Roll, move, apply obstacle, "
            "if you go past the end you stay put. Land exactly on the last cell to win and leave the queue."
        ),
        "cast": [
            ("Game", "The host - setup, turn loop, winner print."),
            ("Board", "Cells + serpentine numbering + obstacles."),
            ("Cell", "A position; maybe has a snake or ladder."),
            ("Player", "Name + current position."),
            ("Dice", "One or more dice summed."),
            ("Obstacle / Snake / Ladder", "Jump from src to dest."),
            ("ObstacleFactory", "Create snake or ladder from type."),
        ],
        "walkthrough": [
            "Input size, snake count, ladder count, players, dice count.",
            "Board created; obstacles placed without overlapping cells.",
            "Turn: pop player from deque, roll dice, compute new position.",
            "If overshoot -> stay, append back to queue.",
            "Else move; if cell has obstacle, jump to dest.",
            "If position == size -> win (do not re-queue). Else re-queue.",
        ],
        "why_patterns": [
            ("Why Factory?", "Board placement code shouldn't care Snake vs Ladder construction details."),
            ("Why polymorphism?", "Cell just asks obstacle for final position - same for snake or ladder."),
        ],
        "boxes": [
            Box("Game loop", ["deque of players", "roll -> move -> win?"]),
            Box("Board", ["serpentine cells", "obstacles"]),
            Box("Snake", ["head -> tail down"]),
            Box("Ladder", ["bottom -> top up"]),
        ],
        "remember": [
            "Must land exactly on last cell.",
            "Ladder constructor args are easy to mix up (top/bottom) - read the class once.",
            "Perfect square board size is assumed.",
        ],
        "oops_simple": [
            ("Encapsulation", "Board hides how row/col mapping works."),
            ("Abstraction", "Obstacle means 'jump somewhere'."),
            ("Inheritance", "Snake and Ladder are Obstacles."),
            ("Polymorphism", "Same move path applies any obstacle on the cell."),
        ],
    },
    "hashmap": {
        "title": "Custom HashMap - How it works",
        "one_liner": "Keys go into buckets by hash. Collisions chain in a list. Too full? Grow and rehash.",
        "story": (
            "Like a set of drawers. hash(key) % number_of_drawers picks the drawer. "
            "Inside the drawer, entries are a linked list (separate chaining). "
            "Each drawer starts with a dummy sentinel node so insert/remove is simpler. "
            "When entries > 0.75 * drawers, double drawers and redistribute everything."
        ),
        "cast": [
            ("CustomHashMap", "put / get / remove. Owns bucket array and count."),
            ("Node", "One entry: key, value, next, prev (doubly linked)."),
            ("Sentinel head", "Dummy node at start of each bucket chain."),
            ("Load factor 0.75", "Trigger for growing the table."),
        ],
        "walkthrough": [
            "put('John', 78): hash -> bucket index.",
            "Walk chain; if key exists, update value.",
            "Else insert new node after sentinel; count++.",
            "If count too high vs capacity -> rehash to 2x buckets.",
            "get('John'): same hash, walk chain, return value or None.",
            "remove: unlink node from its neighbors, count--.",
        ],
        "why_patterns": [
            ("Why sentinel?", "Fewer special cases for empty bucket / remove head."),
            ("Why doubly linked?", "Once you found the node, unlinking is O(1)."),
            ("Why rehash?", "Keep average chain short so get/put stay fast."),
        ],
        "boxes": [
            Box("Bucket array", ["index = hash % n", "each has sentinel"]),
            Box("Chain", ["Node <-> Node", "key, value"]),
            Box("put", ["find or insert", "maybe rehash"]),
            Box("get / remove", ["walk chain", "unlink"]),
        ],
        "remember": [
            "Average O(1); worst O(n) if everything collides.",
            "Python hash() is not stable across processes.",
            "remove does not shrink the table in this demo.",
        ],
        "oops_simple": [
            ("Encapsulation", "You only call put/get/remove - buckets stay private."),
            ("Abstraction", "HashMap ADT hides collision handling."),
            ("Inheritance", "Not the main tool here - composition of nodes."),
            ("Polymorphism", "Works for any hashable key type via generics."),
        ],
    },
}


class NotesPDF(FPDF):
    """Compact home-notes PDF to save pages when printing."""

    def __init__(self, title: str) -> None:
        super().__init__(format="A4")
        self.doc_title = title
        self.set_auto_page_break(auto=True, margin=10)
        self.add_font("Body", "", FONT)
        self.add_font("Body", "B", FONT_BOLD if Path(FONT_BOLD).exists() else FONT)
        self.set_margins(10, 10, 10)

    def header(self) -> None:
        if self.page_no() == 1:
            return
        self.set_font("Body", "", 7)
        self.set_text_color(120, 120, 120)
        self.set_x(self.l_margin)
        self.cell(0, 4, safe(f"Home notes | {self.doc_title}"), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(210, 210, 210)
        self.line(self.l_margin, self.get_y(), 200, self.get_y())
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def footer(self) -> None:
        self.set_y(-9)
        self.set_font("Body", "", 7)
        self.set_text_color(130, 130, 130)
        self.cell(0, 6, f"{self.page_no()}/{{nb}}", align="C")

    def h1(self, t: str) -> None:
        self.set_x(self.l_margin)
        self.set_font("Body", "B", 13)
        self.multi_cell(0, 6, safe(t))
        self.set_x(self.l_margin)
        self.ln(0.5)

    def h2(self, t: str) -> None:
        self.ln(1)
        self.set_x(self.l_margin)
        self.set_font("Body", "B", 10)
        self.set_fill_color(245, 247, 250)
        self.multi_cell(0, 5.5, safe(f" {t}"), fill=True)
        self.set_x(self.l_margin)
        self.ln(1)

    def para(self, t: str) -> None:
        self.set_x(self.l_margin)
        self.set_font("Body", "", 8.5)
        self.multi_cell(0, 4.2, safe(t))
        self.set_x(self.l_margin)

    def bullet(self, t: str) -> None:
        self.set_x(self.l_margin)
        self.set_font("Body", "", 8.5)
        self.multi_cell(0, 4.0, safe(f"- {t}"))
        self.set_x(self.l_margin)

    def numbered(self, n: int, t: str) -> None:
        self.set_x(self.l_margin)
        self.set_font("Body", "", 8.5)
        self.multi_cell(0, 4.0, safe(f"{n}. {t}"))
        self.set_x(self.l_margin)

    def kv(self, key: str, val: str) -> None:
        """Compact cast line: Name - role."""
        self.set_x(self.l_margin)
        self.set_font("Body", "", 8.5)
        self.multi_cell(0, 4.0, safe(f"{key}: {val}"))
        self.set_x(self.l_margin)

    def callout(self, title: str, body: str, fill=NOTE_FILL) -> None:
        self.set_x(self.l_margin)
        self.set_fill_color(*fill)
        self.set_draw_color(190, 190, 190)
        self.set_font("Body", "B", 8.5)
        self.multi_cell(0, 4.5, safe(f"{title} — {body}"), fill=True, border=1)
        self.set_x(self.l_margin)
        self.ln(1.5)

    def draw_boxes(self, boxes: Sequence[Box]) -> None:
        cols = 2
        gap = 3
        usable = 200 - self.l_margin
        w = (usable - gap) / cols
        x0 = [self.l_margin, self.l_margin + w + gap]
        y_col = [self.get_y(), self.get_y()]

        for i, box in enumerate(boxes):
            c = i % cols
            lines = [safe(x) for x in box.lines]
            h = 6.5 + max(len(lines), 1) * 3.8 + 2
            if y_col[c] + h > self.page_break_trigger:
                self.add_page()
                y_col = [self.get_y(), self.get_y()]
            x, y = x0[c], y_col[c]
            self.set_draw_color(*BOX_BORDER)
            self.set_fill_color(*BOX_FILL)
            self.rect(x, y, w, h, style="DF")
            self.set_xy(x + 1.5, y + 1)
            self.set_font("Body", "B", 8)
            self.cell(w - 3, 4, safe(box.title)[:44])
            self.line(x + 1.5, y + 5.5, x + w - 1.5, y + 5.5)
            self.set_font("Body", "", 7)
            yy = y + 6.2
            for line in lines:
                self.set_xy(x + 2, yy)
                self.cell(w - 4, 3.6, f"- {line}"[:56])
                yy += 3.6
            y_col[c] = y + h + gap

        self.set_y(max(y_col) + 0.5)
        self.set_x(self.l_margin)


def render_full_md(pdf: NotesPDF, md_path: Path) -> None:
    """Include the full DESIGN.md file content in the PDF."""
    if not md_path.exists():
        pdf.para("(DESIGN.md not found in this folder)")
        return

    pdf.callout(
        "Full DESIGN.md (same file as in this folder)",
        str(md_path.name),
        STEP_FILL,
    )

    text = md_path.read_text(encoding="utf-8")
    parts = re.split(r"\n(?=## )", text)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if part.startswith("# "):
            lines = part.splitlines()
            # Print title + intro lines under H1, then subsections
            pdf.h2(lines[0][2:].strip())
            intro = []
            rest_start = 1
            for i, ln in enumerate(lines[1:], 1):
                if ln.startswith("## "):
                    rest_start = i
                    break
                intro.append(ln)
                rest_start = i + 1
            _flush_md_body(pdf, intro)
            rest = "\n".join(lines[rest_start:]).strip()
            for sub in re.split(r"\n(?=## )", rest):
                _one_md_section(pdf, sub)
            continue
        _one_md_section(pdf, part)


def _one_md_section(pdf: NotesPDF, section: str) -> None:
    lines = section.splitlines()
    if not lines:
        return
    if lines[0].startswith("## "):
        pdf.h2(lines[0][3:].strip())
        body = lines[1:]
    else:
        body = lines
    _flush_md_body(pdf, body)


def _flush_md_body(pdf: NotesPDF, body: list[str]) -> None:
    buf: list[str] = []
    in_code = False
    code: list[str] = []

    def flush() -> None:
        nonlocal buf
        raw = "\n".join(buf).strip()
        buf = []
        if not raw:
            return
        raw = re.sub(r"\*\*(.+?)\*\*", r"\1", raw)
        raw = re.sub(r"`([^`]+)`", r"\1", raw)
        if raw.lstrip().startswith("|"):
            for row in raw.splitlines():
                if re.match(r"^\|?\s*-+", row):
                    continue
                cells = [c.strip() for c in row.strip("|").split("|") if c.strip()]
                if not cells:
                    continue
                if len(cells) >= 2:
                    pdf.bullet(f"{cells[0]} — {' | '.join(cells[1:])}")
                else:
                    pdf.bullet(cells[0])
            return
        for ln in raw.splitlines():
            ln = ln.strip()
            if not ln or ln == "---":
                continue
            ln = re.sub(r"^[-*]\s+", "", ln)
            ln = re.sub(r"^\d+\.\s+", "", ln)
            ln = re.sub(r"^\*\*A\.\*\*\s*", "A. ", ln)
            ln = re.sub(r"^A\.\s*", "A. ", ln)
            pdf.para(ln)

    for line in body:
        if line.strip().startswith("```"):
            if in_code:
                pdf.set_x(pdf.l_margin)
                pdf.set_font("Body", "", 6.5)
                pdf.set_fill_color(248, 248, 248)
                pdf.multi_cell(0, 3.2, safe("\n".join(code)), border=1, fill=True)
                pdf.set_x(pdf.l_margin)
                pdf.ln(1)
                code = []
                in_code = False
            else:
                flush()
                in_code = True
            continue
        if in_code:
            code.append(line)
            continue
        if line.startswith("### "):
            flush()
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Body", "B", 8.5)
            pdf.multi_cell(0, 4.2, safe(line[4:].strip()))
            pdf.set_x(pdf.l_margin)
            continue
        buf.append(line)
    if in_code and code:
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Body", "", 6.5)
        pdf.set_fill_color(248, 248, 248)
        pdf.multi_cell(0, 3.2, safe("\n".join(code)), border=1, fill=True)
        pdf.set_x(pdf.l_margin)
    flush()


def collect_source_files(slug: str) -> list[Path]:
    """All .py files in the project, main.py first, skip __pycache__ / __init__ empty noise."""
    root = LLD / slug
    files = [
        p for p in root.rglob("*.py")
        if "__pycache__" not in p.parts
    ]

    def sort_key(p: Path) -> tuple:
        rel = p.relative_to(root).as_posix()
        # Prefer reading order for learning
        rank = 50
        if rel == "main.py":
            rank = 0
        elif "/service/" in rel or rel.startswith("service/"):
            rank = 1
        elif "/model/" in rel or rel.startswith("model/"):
            rank = 2
        elif "/strategy/" in rel or rel.startswith("strategy/"):
            rank = 3
        elif "/state/" in rel or rel.startswith("state/"):
            rank = 3
        elif "/cor/" in rel or rel.startswith("cor/"):
            rank = 3
        elif "/limiter/" in rel or rel.startswith("limiter/"):
            rank = 3
        elif "/factory/" in rel or rel.startswith("factory/"):
            rank = 4
        elif "/repository/" in rel or rel.startswith("repository/"):
            rank = 5
        elif rel.endswith("__init__.py"):
            rank = 90
        return (rank, rel)

    files.sort(key=sort_key)
    # Drop empty __init__.py files to save pages
    out: list[Path] = []
    for p in files:
        text = p.read_text(encoding="utf-8", errors="replace").strip()
        if p.name == "__init__.py" and (not text or text == '"""Package."""' or len(text) < 40):
            continue
        out.append(p)
    return out


def render_source_code(pdf: NotesPDF, slug: str) -> None:
    """Append project source code in a compact printable form."""
    files = collect_source_files(slug)
    pdf.add_page()
    pdf.h1(f"Source code — lld/{slug}/")
    pdf.para(
        f"{len(files)} Python files below (compact font to save pages). "
        "Read with the notes: find the class name from the cast, then open that file here."
    )
    pdf.bullet("Tip: start at main.py, then service/, then model/ + strategy/.")

    root = LLD / slug
    for path in files:
        rel = path.relative_to(root).as_posix()
        raw = path.read_text(encoding="utf-8", errors="replace")
        # Normalize tabs, strip trailing spaces; keep content intact
        lines = [ln.rstrip().replace("\t", "    ") for ln in raw.splitlines()]
        if not any(lines):
            continue

        # File header
        if pdf.get_y() > pdf.page_break_trigger - 20:
            pdf.add_page()
        pdf.ln(1)
        pdf.set_x(pdf.l_margin)
        pdf.set_fill_color(40, 60, 90)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Body", "B", 8)
        pdf.multi_cell(0, 5, safe(f" FILE: {rel}  ({len(lines)} lines)"), fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_x(pdf.l_margin)

        # Print code in chunks so multi_cell doesn't choke on huge blocks
        pdf.set_font("Body", "", 6)
        pdf.set_fill_color(250, 250, 250)
        chunk: list[str] = []
        chunk_start = 1

        def emit_chunk(start: int, chunk_lines: list[str]) -> None:
            if not chunk_lines:
                return
            numbered = []
            for i, ln in enumerate(chunk_lines):
                # Truncate extremely long lines for page width
                if len(ln) > 110:
                    ln = ln[:107] + "..."
                numbered.append(f"{start + i:3d}| {safe(ln)}")
            block = "\n".join(numbered)
            # Estimate height; page-break if needed
            est = len(chunk_lines) * 2.7 + 4
            if pdf.get_y() + min(est, 40) > pdf.page_break_trigger:
                pdf.add_page()
                pdf.set_x(pdf.l_margin)
                pdf.set_font("Body", "B", 7)
                pdf.set_text_color(80, 80, 80)
                pdf.multi_cell(0, 4, safe(f"(cont.) {rel}"))
                pdf.set_text_color(0, 0, 0)
                pdf.set_x(pdf.l_margin)
                pdf.set_font("Body", "", 6)
            pdf.set_x(pdf.l_margin)
            pdf.set_fill_color(250, 250, 250)
            pdf.multi_cell(0, 2.7, block, fill=True)
            pdf.set_x(pdf.l_margin)

        for i, ln in enumerate(lines, 1):
            chunk.append(ln)
            # Flush every ~45 lines to keep layout stable
            if len(chunk) >= 45:
                emit_chunk(chunk_start, chunk)
                chunk_start = i + 1
                chunk = []
        emit_chunk(chunk_start, chunk)


def build_pdf(slug: str, meta: dict) -> Path:
    out = LLD / slug / "DESIGN.pdf"
    md_path = LLD / slug / "DESIGN.md"
    pdf = NotesPDF(meta["title"])
    pdf.alias_nb_pages()

    # ---- Compact home notes ----
    pdf.add_page()
    pdf.set_font("Body", "B", 14)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 6.5, safe(meta["title"]), align="C")
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Body", "", 8.5)
    pdf.multi_cell(
        0, 4,
        "Home notes + DESIGN.md + source code  |  compact print",
        align="C",
    )
    pdf.set_x(pdf.l_margin)
    pdf.ln(2)

    pdf.callout("In one line", meta["one_liner"], STEP_FILL)
    pdf.h2("Story — how this LLD works")
    pdf.para(meta["story"])

    pdf.h2("Who does what")
    for name, role in meta["cast"]:
        pdf.kv(name, role)

    pdf.h2("Main pieces")
    pdf.draw_boxes(meta["boxes"])

    pdf.h2("Step-by-step at runtime")
    for i, step in enumerate(meta["walkthrough"], 1):
        pdf.numbered(i, step)

    pdf.h2("Why this design (plain words)")
    for title, body in meta["why_patterns"]:
        pdf.callout(title, body, NOTE_FILL)

    pdf.h2("Remember")
    for tip in meta["remember"]:
        pdf.bullet(tip)

    pdf.h2("OOP in this project")
    for title, body in meta["oops_simple"]:
        pdf.callout(title, body, BOX_FILL)

    # ---- Full DESIGN.md ----
    pdf.add_page()
    pdf.h1("DESIGN.md — full file")
    pdf.para(
        f"Complete markdown from lld/{slug}/DESIGN.md (Q&A for learning)."
    )
    render_full_md(pdf, md_path)

    # ---- Full source code ----
    render_source_code(pdf, slug)

    pdf.output(str(out))
    return out


def main() -> None:
    if not Path(FONT).exists():
        raise SystemExit(f"Font not found: {FONT}")
    for slug, meta in PROJECTS.items():
        path = build_pdf(slug, meta)
        print(f"Wrote {path.relative_to(ROOT)}")

    index = LLD / "ALL_LLD_DESIGN_NOTEBOOKS.pdf"
    pdf = NotesPDF("All LLD home notes")
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.h1("LLD Home Notes - Index")
    pdf.para(
        "Each DESIGN.pdf = how-it-works notes + full DESIGN.md + project source code. "
        "Print double-sided to save paper."
    )
    for i, (slug, meta) in enumerate(PROJECTS.items(), 1):
        n_files = len(collect_source_files(slug))
        pdf.bullet(f"{i}. {meta['title']} -> lld/{slug}/DESIGN.pdf  ({n_files} code files)")
        pdf.para(meta["one_liner"])
    pdf.output(str(index))
    print(f"Wrote {index.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
