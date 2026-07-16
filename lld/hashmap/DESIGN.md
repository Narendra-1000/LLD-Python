# Designing a Custom HashMap — LLD Q&A

**Run:** `python -m lld.hashmap.main`  
**Focus:** Data structure internals (not classic GoF patterns)

---

## Q1. What problem are we solving?

**A.** Implement a **hash map from scratch** with:

1. Generic key-value storage (`CustomHashMap[K, V]`)
2. **Separate chaining** for collisions
3. **Dynamic resizing** when load factor is exceeded
4. `get` / `put` / `remove` with average O(1)

Similar spirit to Java `HashMap` bucket chains.

---

## Q2. What are the core pieces?

| Class | Responsibility |
|-------|----------------|
| `Node[K, V]` | Doubly-linked list node: key, val, next, prev |
| `CustomHashMap[K, V]` | Bucket array, chaining, rehash |

---

## Q3. How is the package structured?

```
hashmap/
├── custom_hash_map.py  # Node + CustomHashMap
└── main.py             # Demo put/get
```

Simple package — pure data-structure LLD, no service/strategy layers.

---

## Q4. How does internal design work?

| Concern | Approach |
|---------|----------|
| **Buckets** | Array of chains; each bucket has a **sentinel head** |
| **Hash** | `hash(key) % bucket_count` |
| **Load factor** | `0.75` — rehash when `count > 0.75 * capacity` |
| **Rehash** | Double capacity (cap `1 << 30`), redistribute nodes |
| **Collisions** | Separate chaining via doubly-linked lists |

Sentinel heads avoid null edge cases on insert/remove.

---

## Q5. How do core operations work?

**put** (amortized O(1))
```
find node by key in bucket
  → exists: update value
  → else: insert after sentinel, count++
  → if over load factor: rehash (2×)
```

**get** (average O(1)) — traverse bucket chain via `find_node`.

**remove** (average O(1)) — unlink from doubly-linked list, decrement count.

---

## Q6. What does the demo show?

```
put several entries → get existing key → get missing key (None)
```

Initial capacity is small (4) for demo; rehash grows as load increases.

---

## Q7. How do you extend this design?

| Add… | How |
|------|-----|
| Custom hash/eq | Accept `hash_fn` / `eq_fn` callables |
| Treeify long chains | Convert chain → tree when length > 8 (Java 8 style) |
| Iteration | `keys()`, `values()`, `items()` |
| Concurrent map | Striping or per-bucket locks |
| Shrink on delete | Rehash down when load drops |

---

## Q8. Common interview follow-ups

**Q. Why doubly-linked lists in buckets?**  
O(1) unlink on remove once the node is found; sentinel simplifies head/tail cases.

**Q. What happens at load factor 0.75?**  
Rehash doubles buckets and redistributes — keeps average chain length low.

**Q. Is Python `hash()` stable?**  
Not across processes (hash randomization) — important if you serialize hash codes.

**Q. Does remove shrink the table?**  
No — only grows on put. Mention shrink as a production enhancement.

**Q. Open addressing vs chaining?**  
This design uses chaining. Open addressing stores entries in the array itself (linear/quadratic probing) — discuss trade-offs if asked.
