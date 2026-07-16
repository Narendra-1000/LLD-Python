# Designing a Rate Limiter — LLD Q&A

**Run:** `python -m lld.rate_limiter.main`  
**Patterns:** Strategy · Factory · Facade/Service · Thread safety

---

## Q1. What problem are we solving?

**A.** Design an API rate limiter that:

1. Enforces per-user request quotas by **subscription tier**
2. Supports multiple **algorithms** (Token Bucket, Fixed Window, Sliding Window Log)
3. Is **thread-safe** under concurrent requests
4. Returns allow / block for each request

---

## Q2. What are the core entities?

| Entity | Responsibility |
|--------|----------------|
| `User` | Identity + tier (FREE / PREMIUM) |
| `RateLimitConfig` | `max_requests`, `window_in_seconds` |
| `RateLimiter` (ABC) | `allow_request(user_id) → bool` |
| `RateLimiterFactory` | Algo enum → concrete limiter |
| `RateLimiterService` | Maps tier → limiter; public API |

**Demo mapping:**  
- FREE → Token Bucket (10 / 60s)  
- PREMIUM → Fixed Window (100 / 60s)

---

## Q3. How is the package structured?

```
rate_limiter/
├── model/       # User, RateLimitConfig
├── limiter/     # TokenBucket, FixedWindow, SlidingWindowLog
├── factory/     # RateLimiterFactory
├── service/     # RateLimiterService
└── enums/       # RateLimitType, UserTier
```

---

## Q4. Why Strategy for algorithms?

**A.** Algorithms differ; callers only need `allow_request`. Swap without changing the service API.

| Algorithm | Idea |
|-----------|------|
| **Token Bucket** | Tokens refill over time; allows short bursts |
| **Fixed Window** | Count requests per fixed time window |
| **Sliding Window Log** | Store timestamps; prune expired; count in window |

Each implementation uses `threading.Lock` on its per-user state.

---

## Q5. Why Factory?

**A.** `RateLimiterFactory.create_rate_limiter(algo, config)` maps enum → class. Service does not hard-code constructors.

---

## Q6. What is the request flow?

```
RateLimiterService.allow_request(user)
  → pick limiter by user.tier
  → limiter.allow_request(user_id)  # under lock
  → True (ALLOWED) / False (BLOCKED)
```

`main.py` stress-tests with 20 concurrent threads → ~10 allowed for FREE token bucket.

---

## Q7. How do the algorithms compare?

| | Token Bucket | Fixed Window | Sliding Window Log |
|---|--------------|--------------|-------------------|
| Burst | Yes | At window edges | Smooth |
| Memory | Low (tokens + last refill) | Low (count + window id) | Higher (timestamp list) |
| Accuracy | Good | Boundary burst problem | Most accurate |

---

## Q8. How do you extend this design?

| Add… | How |
|------|-----|
| Leaky Bucket / Sliding Counter | New limiter class + factory case (enums already hint at these) |
| Per-endpoint limits | Key = `user_id + endpoint` |
| Distributed limiting | Redis INCR/EXPIRE or Redis cell |
| Retry metadata | Return `remaining`, `retry_after` instead of bool |

---

## Q9. Common interview follow-ups

**Q. Fixed window boundary burst?**  
User can send `max` at end of window W1 and `max` at start of W2 → 2× limit in a short span. Sliding window fixes this.

**Q. Token bucket refill rate in this code?**  
`window / max_requests` seconds per token (inverted from "tokens per second" wording — know both formulations).

**Q. Multi-server?**  
In-memory state is per process — need Redis (or similar) for cluster-wide limits.
