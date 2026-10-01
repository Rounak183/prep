# Amazon SDE2 Prep Notes (Concepts + Revision)

This file is a running notebook for concepts learned during the sprint. It is designed for quick review before the interview.

---

## Day 1: Caching + Redis (Step-by-Step Guide)

### 1) What Caching Is (and Why It Exists)

**Definition:**  
Caching is storing frequently accessed data in a faster layer (usually memory) to reduce latency and backend load.

**Why it matters:**  
- Faster response times (lower p95/p99 latency)
- Reduced database load
- Better scalability during spikes

---

### 2) Core Caching Patterns

**Cache-Aside (Lazy Loading)**
1. App checks cache for key.
2. If hit, return value.
3. If miss, read from DB.
4. Store result in cache with TTL.
5. Return value.

**Pros:** Simple, resilient.  
**Cons:** First read is a miss; stale data possible.

**Write-Through**
1. App writes to cache and DB at the same time.
2. Cache always has latest data.

**Pros:** Fresh cache.  
**Cons:** Writes are slower; cache fills with cold data.

**Write-Behind (Write-Back)**
1. App writes to cache only.
2. Cache asynchronously writes to DB later.

**Pros:** Fast writes.  
**Cons:** Risk of data loss on cache failure.

---

### 3) Cache Invalidation (The Hard Part)

**Key strategies:**
- **TTL (Time-to-Live):** Auto-expire data after N seconds.
- **Write-Invalidate:** On update, delete cache key.
- **Write-Update:** On update, refresh cache key.

**Rule of thumb:**  
If consistency is critical, prefer **write-invalidate** + short TTL.

---

### 4) When to Cache

Good candidates:
- Read-heavy data (user profiles, product catalogs)
- Expensive computations
- Hot keys with frequent repeated access

Avoid caching:
- Highly volatile data
- Sensitive data without encryption or strict controls

---

### 5) Redis Basics (What It Is)

**Redis** = in-memory data store used for caching, counters, rate limiting, sessions, pub/sub, and more.

**Key features:**
- Very fast (memory)
- Supports multiple data structures
- TTL support per key
- Optional persistence

Common structures:
- **String** (simple key-value)
- **Hash** (object fields)
- **List** (queues)
- **Set** (unique items)
- **Sorted Set** (leaderboards, ranking)

---

### 6) Redis in System Design (Typical Uses)

- **Cache layer** in front of DB
- **Rate limiting** (token bucket, fixed window)
- **Session store**
- **Leaderboard / ranking**
- **Job queues** (Lists)

---

### 7) Cache Stampede & Hot Keys

**Cache Stampede:** Many clients miss cache at once and hit DB (e.g., a popular key expires and thousands of requests fall through simultaneously).

Fixes:
- **Request coalescing** (one fetch populates cache)
- **Randomized TTL (jitter):** Add small random offsets to TTL so keys don’t expire at the same time.
- **Early refresh** (refresh before expiration)
- **Mutex/Distributed lock:** Use `SETNX`-style locks so only one worker refreshes a hot key.

**Hot keys:** One key is accessed disproportionately.

Fixes:
- **Key sharding** (split one key into many)
- **Local in-process cache** for that key

---

### 8) Redis Consistency + Persistence (Know the Trade-offs)

**Persistence options:**
- **RDB snapshots:** Periodic point-in-time snapshots of the dataset.
- **AOF (Append-Only File):** Logs every write; **slower but more durable** than RDB.

**Key trade-off:**  
More durability = lower speed.

**Takeaway for interview:**  
Redis as cache is typically **best-effort** (not source of truth).

---

### 9) Where Redis Sits in Architecture

```
Client -> App/API -> Redis Cache -> Database
```

**Say this clearly:**  
“Redis sits between the application and database as a distributed cache.”

---

### 10) Read vs Write Behavior

- **Read-heavy system:** caching is very effective.
- **Write-heavy system:** cache benefit decreases.

**Interview line:**  
“Caching helps most when the read-to-write ratio is high.”

---

### 11) Consistency Trade-off

- Cache introduces **eventual consistency**.
- **Database is the source of truth**.
- Cache may lag behind writes.

**Interview line:**  
“We accept eventual consistency for better latency.”

---

### 12) Scaling Redis

- **Vertical scaling:** limited.
- **Horizontal scaling (Redis Cluster):** data sharded across nodes.
- **Replication:** primary + replicas for read scaling and HA.

**Interview line:**  
“I’d use Redis Cluster with sharding and replicas for high availability.”

---

### 13) Failure Handling (When Redis Is Down)

- **Fallback to DB** (higher latency temporarily).
- Protect DB with **circuit breaker** and **rate limiting**.

**Interview line:**  
“System should degrade gracefully if cache is unavailable.”

---

### 14) Cache Key Design

- Use clear naming: `user:123`, `product:456`
- Avoid collisions.
- Keep keys predictable.

---

### 15) Interview Sound Bites (Use These)

- “I’d use cache-aside with TTL + write-invalidate for consistency.”  
- “For hot keys, I’d shard and add jitter to TTL to prevent stampede.”  
- “Redis is great for fast reads but shouldn’t be the source of truth.”  
- “If writes are heavy, cache might not help much.”

---

### 16) Quick Practice Prompts (Self-Test)

1. When would you use write-through vs cache-aside?
2. How do you prevent cache stampede?
3. What Redis data structure for a leaderboard?
4. What’s the downside of write-behind?
5. How do you handle stale data in cache?

---

### 16a) Quick Answers

1. **Write-through vs cache-aside:**  
   Use **write-through** when you need fresher cache reads and can tolerate slower writes.  
   Use **cache-aside** as the default for simplicity and when occasional stale reads are acceptable.

2. **Prevent cache stampede:**  
   Use **TTL jitter**, **request coalescing**, **early refresh**, and **distributed locks** (`SETNX`) for hot keys.

3. **Redis structure for leaderboard:**  
   **Sorted Set (ZSET)** — it supports score ordering and range queries.

4. **Downside of write-behind:**  
   **Risk of data loss** if cache crashes before async write flushes to DB.

5. **Handle stale cache:**  
   **Write-invalidate** on updates, **short TTLs**, and **background refresh** for hot data.

---

### 17) One-Page Summary (5-Minute Review)

- Cache speeds reads and reduces DB load.
- Cache-aside is default; write-through for strong freshness.
- Invalidation is the hardest part; TTL + write-invalidate is common.
- Redis offers TTL + data structures; best-effort cache.
- Watch for stampede and hot keys; use jitter + sharding.

---

### 18) 20-Second High-Signal Answer (Practice)

“I’d start with a cache-aside strategy using Redis with TTL and write-invalidation. Since this is a read-heavy system, caching will significantly reduce DB load. I’d add jitter to TTLs to prevent stampede and use Redis Cluster with sharding and replicas for availability. The system is eventually consistent, which is acceptable for this use case.”

---

## Day 2: Load Balancers + Rate Limiting (Step-by-Step Guide)

### 1) What a Load Balancer Does

**Definition:**  
A load balancer distributes incoming traffic across multiple servers to improve availability, latency, and throughput.

**Why it matters:**  
- Prevents single server overload  
- Enables horizontal scaling  
- Improves fault tolerance

---

### 2) Where It Sits in Architecture

```
Client -> Load Balancer -> App Servers -> DB/Cache
```

**Say this clearly:**  
“The load balancer sits between clients and app servers to distribute traffic and provide high availability.”

---

### 3) Common Load Balancing Algorithms

- **Round Robin:** simple, equal distribution.  
- **Least Connections:** send traffic to the least busy server.  
- **IP Hash:** consistent client-to-server routing (useful for sticky sessions).  

**Interview line:**  
“I’d start with round robin, then move to least-connections if workloads are uneven.”

---

### 4) Health Checks (Critical for HA)

**Why:** Remove unhealthy servers automatically.  
**How:** Periodic heartbeat/ping; if failed, remove from rotation.

**Interview line:**  
“Health checks ensure traffic only goes to healthy instances.”

---

### 5) L4 vs L7 Load Balancing

- **L4 (TCP/UDP):** faster, no content inspection.  
- **L7 (HTTP):** can route by path, headers, or cookies.  

**Interview line:**  
“Use L7 when you need smart routing; L4 for raw speed.”

---

### 6) Sticky Sessions (When to Use)

**Sticky sessions** keep a client bound to the same server.  
Use only if session state isn’t externalized.

**Better:** Store sessions in Redis or DB to avoid stickiness.

---

## Rate Limiting

### 7) What Rate Limiting Does

**Definition:**  
Limits how many requests a user/service can make in a time window.

**Why it matters:**  
- Prevents abuse/spikes  
- Protects downstream services  
- Ensures fair usage

---

### 8) Common Rate Limiting Algorithms

- **Fixed Window:** simple, can allow bursts at window edge.  
- **Sliding Window:** smoother, more accurate.  
- **Token Bucket:** allows bursts up to bucket size.  
- **Leaky Bucket:** smooths traffic, steady flow.

**Interview line:**  
“Token bucket is a good default because it allows controlled bursts.”

**Simple explanations (easy to remember):**

- **Fixed Window:**  
  Count requests in a fixed time box (e.g., 100/min).  
  Problem: users can burst at the end and start of a window.

- **Sliding Window:**  
  Like fixed window, but checks the last N seconds continuously.  
  Smoother, fewer bursts, more accurate.

- **Token Bucket:**  
  Tokens refill at a steady rate. Each request spends a token.  
  If tokens are saved up, you can burst; if empty, requests are blocked.

- **Leaky Bucket:**  
  Requests go into a bucket and leak out at a fixed rate.  
  This smooths traffic into a steady stream.

---

### 8a) Choosing the Right Algorithm (Practical View)

- **Token Bucket:** best default, allows controlled bursts.  
- **Leaky Bucket:** strict smoothing (payments, critical APIs).  
- **Sliding Window:** fairness-critical systems (uniform rate over time).

---

### 9) Where to Enforce Rate Limits

- **API Gateway / Edge** (best place)  
- **Load Balancer layer**  
- **App layer** (fallback)

**Interview line:**  
“I’d enforce limits at the edge to protect all downstream services.”

**What does “edge” mean?**  
The **edge** is the first entry point into your system — usually an API gateway, CDN, or reverse proxy that receives traffic before app servers.

**What are “downstream services”?**  
Everything behind the edge: **app servers, caches, databases, and internal services**. They’re “downstream” because requests flow **from edge → deeper systems**.

---

### 10) Storing Counters

Use **Redis** for fast counters with TTL.  
- Key format: `rate:user:123`  
- TTL aligns with window  
- Atomic ops (e.g., `INCR`)

**Simple example (Fixed Window: 100 requests/min):**
1. User `123` makes a request.
2. App runs `INCR rate:user:123`.
3. If count > 100, block request.
4. Set `TTL = 60s` so the counter resets each minute.

**Why this works:**
- TTL auto-resets the window.
- `INCR` is atomic, so concurrent requests are counted correctly.

---

### 10a) Distributed Rate Limiting (SDE2 Signal)

**Problem:** Multiple app servers mean counters must be consistent globally.  
**Solution:** Use a centralized store like **Redis** with atomic ops (`INCR`).  

**Interview line:**  
“Rate limiting must be consistent across instances, so I’d use Redis for shared counters.”

---

### 10b) Abuse & DDoS Protection (Beyond Rate Limits)

- **Rate limiting** is the first layer.  
- Add **IP blocking**, **CAPTCHA**, and a **WAF (Web Application Firewall)** at the edge.

**Interview line:**  
“Rate limiting helps, but at scale I’d combine it with WAF and filtering at the edge.”

---

### 10c) Retries & Idempotency (Important Edge Case)

- Clients may retry failed requests.  
- Ensure **idempotency** to avoid duplicate effects (especially payments).

**Example:**  
Use idempotency keys for payment APIs.

---

### 11) Failure Handling

- If Redis is down: fail-open (allow) or fail-closed (block).  
- For Amazon, **fail-open** is often safer to avoid outages, but depends on abuse risk.

**Interview line:**  
“Rate limiting should degrade gracefully; choose fail-open vs fail-closed based on abuse risk.”

---

### 12) Interview Sound Bites (Use These)

- “Load balancers improve availability and smooth traffic spikes.”  
- “L7 lets you route based on URL, headers, or cookies.”  
- “Rate limiting protects backends and ensures fairness.”  
- “Token bucket is a great default when you want burst tolerance.”

---

### 13) Quick Practice Prompts (Self-Test)

1. When would you choose L7 over L4?
2. What problem does sticky sessions create?
3. Fixed window vs sliding window: trade-off?
4. Where should rate limiting live?
5. How would you implement counters in Redis?

---

### 13a) Quick Answers

1. **L7 over L4:**  
   Choose **L7** when you need routing by **URL/path, headers, cookies**, or content-based rules. Use **L4** for raw speed and simple TCP/UDP forwarding.

2. **Sticky sessions problem:**  
   They reduce flexibility and fault tolerance because a user is tied to one server. If that server fails, sessions break unless state is externalized.

3. **Fixed vs sliding window trade-off:**  
   **Fixed window** is simpler but allows bursty traffic at window edges.  
   **Sliding window** is smoother and fairer but more complex to implement.

4. **Where should rate limiting live:**  
   **At the edge/API gateway** first, then optionally at the app layer as a fallback.

5. **Counters in Redis:**  
   Use atomic **`INCR`** with a **TTL** on a key like `rate:user:123`.  
   TTL aligns with the time window.

---

### 14) 20-Second High-Signal Answer (Practice)

“I’d put an L7 load balancer in front of stateless app servers with health checks. For rate limiting, I’d use a token bucket stored in Redis at the API gateway. That protects downstream services and still allows controlled bursts. If Redis fails, I’d decide fail-open vs fail-closed based on abuse risk.”

---

### 14a) 20-Second High-Signal Answer (Upgraded)

“I’d use a managed L7 load balancer to route traffic to stateless app servers with health checks. At scale, I’d add global load balancing for latency-based routing. For rate limiting, I’d implement a token bucket at the API gateway using Redis for distributed counters. This protects downstream services while allowing controlled bursts, and I’d handle Redis failures with a fail-open or fail-closed strategy depending on abuse risk.”

---

### 15) Types of Load Balancers

- **Software LB:** e.g., Nginx (flexible, common).  
- **Managed LB:** e.g., AWS ELB (scalable, managed).  
- **Hardware LB:** high performance, less common today.

**Interview line:**  
“In practice, I’d use a managed load balancer like AWS ELB for scalability and reliability.”

---

### 16) Global vs Regional Load Balancing

- **Global LB:** routes users to the closest region (latency-based).  
- **Regional LB:** distributes traffic within a region.

**Interview line:**  
“At scale, I’d use global load balancing to route users to the nearest region, then a regional LB internally.”

---

### 17) Stateless App Servers

- App servers should be **stateless**.  
- Store session data in **Redis** or **DB**.

**Interview line:**  
“Stateless services allow the load balancer to route requests freely.”

---

## Day 3: Consistent Hashing + Sharding (Step-by-Step Guide)

### 1) What Sharding Is

**Definition:**  
Sharding is splitting data across multiple nodes/partitions to scale storage and throughput.

**Why it matters:**  
- Avoids single-node bottlenecks  
- Enables horizontal scaling  
- Reduces hot-spot pressure

---

### 2) Sharding Strategies

- **Range-based:** shard by key ranges (e.g., user_id 1–1M).  
- **Hash-based:** shard by hash(key) to spread evenly.  
- **Directory-based:** lookup service maps keys to shards.

**Interview line:**  
“Hash-based sharding is common to evenly distribute load.”

**Trade-offs (SDE2 depth):**
- **Range-based:**  
  ✅ Great for range queries  
  ❌ Hotspot risk if keys are skewed
- **Hash-based:**  
  ✅ Even distribution  
  ❌ Harder to support range queries

---

### 3) The Problem: Rebalancing

With mod N hashing, adding one node can **remap almost all keys**, causing cache misses and heavy data migration.

---

### 4) Consistent Hashing (Core Idea)

**Goal:** Minimize key movement when nodes change.  
Keys are placed on a hash ring; each key maps to the **next node clockwise**.

**Key benefit:**  
Only ~1/N keys move when a node is added or removed.

---

### 5) Virtual Nodes (VNodes)

**Problem:** Real nodes can be uneven.  
**Solution:** Assign multiple virtual positions per node on the ring.

**Result:**  
Better balance and smoother rebalancing.

---

### 6) Hot Keys + Mitigations

- **Problem:** Some keys get far more traffic.  
- **Fixes:** key salting, sharding hot keys, or caching hot items separately.

---

### 7) Consistent Hashing in Practice

Common uses:
- **Distributed caches** (Redis cluster, Memcached)  
- **Load distribution** across services  
- **Database sharding**

**Real-world systems:**  
Redis Cluster, Memcached, Apache Cassandra.

---

### 8) Replication + Fault Tolerance

- Store each key on **multiple nodes** (replication factor).  
- If one node fails, requests can fail over to replicas.

**Failure handling detail:**  
If a node fails, traffic can route to the **next node in the ring** or to **replicas**.  
Some systems use **quorum reads/writes** depending on consistency needs.

---

### 9) Interview Sound Bites (Use These)

- “Consistent hashing reduces rebalancing when nodes change.”  
- “Virtual nodes smooth distribution and reduce hotspots.”  
- “Replication + consistent hashing improves fault tolerance.”

---

### 10) Quick Practice Prompts (Self-Test)

1. Why is consistent hashing better than simple hash mod N?
2. What are virtual nodes and why do they help?
3. How would you handle hot keys?
4. What happens when a shard goes down?

---

### 10a) Quick Answers

1. **Consistent hashing vs mod N:**  
   With mod N, adding/removing a node reshuffles most keys.  
   Consistent hashing moves only ~1/N keys, minimizing rebalancing.

2. **Virtual nodes (vnodes):**  
   Multiple virtual positions per physical node on the hash ring.  
   They smooth distribution and reduce hotspots.

3. **Handling hot keys:**  
   Use key salting, shard hot keys across multiple buckets, or add a local cache layer.

4. **Shard failure:**  
   Requests to that shard fail unless you have **replicas**.  
   With replication, fail over to a replica and rebalance when the node returns.

---

### 11) 20-Second High-Signal Answer (Practice)

“I’d use hash-based sharding with consistent hashing to minimize rebalancing when nodes change. I’d add virtual nodes to ensure even distribution, and replication for fault tolerance. For hot keys, I’d shard them further, use key salting, or cache them separately. If range queries are required, I’d consider range-based sharding instead.”

---

## Day 4 (Long): Data Modeling + SQL vs NoSQL (Step-by-Step Guide)

### 1) Start With Requirements (Always First)

Ask:
- **What are the primary read/write patterns?**
- **Is strong consistency required?**
- **What scale (QPS, storage)?**
- **Do we need complex queries/joins?**

**Interview line:**  
“I start with access patterns, then choose the data model and database.”

---

### 2) SQL vs NoSQL (High-Level)

**SQL (Relational):**
- Schema-first, normalized tables
- Strong consistency, ACID transactions
- Great for joins and complex queries

**NoSQL (Non-Relational):**
- Flexible schema
- High scale, high write throughput
- Denormalized data, limited joins

**Interview line:**  
“SQL for complex relational queries and strong consistency; NoSQL for scale and flexibility.”

---

### 3) SQL Pros / Cons (SDE2 Depth)

**Pros:**
- Strong consistency (ACID)
- Rich query support
- Joins/aggregations are easy

**Cons:**
- Harder to scale writes
- Schema changes can be costly

---

### 4) NoSQL Pros / Cons (SDE2 Depth)

**Pros:**
- Horizontal scaling is easier
- High throughput (writes/reads)
- Flexible schema

**Cons:**
- Weaker consistency (often eventual)
- Complex queries require denormalization
- App logic is more complex

---

### 5) Data Modeling Approach (Practical Steps)

1. **List core entities** (User, Order, Product, etc.)
2. **Identify relationships** (1-1, 1-M, M-M)
3. **Map access patterns** (top 5 queries)
4. **Choose model** (normalized vs denormalized)
5. **Add indexes** for high-frequency queries

**Interview line:**  
“I model for access patterns, not just for entities.”

---

### 6) Normalization vs Denormalization

**Normalization (SQL):**
- Reduces duplication
- Keeps data consistent
- Can require joins

**Denormalization (NoSQL):**
- Faster reads
- More duplication
- Writes become heavier

**Interview line:**  
“I normalize for correctness, denormalize for speed when reads dominate.”

**Brief note on Normal Forms (NF):**
- **1NF:** Atomic values, no repeating groups.  
- **2NF:** 1NF + no partial dependency on a composite key.  
- **3NF:** 2NF + no transitive dependencies (non-key depends only on key).

**Normalized table (example):**  
Users and Orders stored separately with foreign keys; minimal duplication.

**Denormalized table (example):**  
Order rows also store user name/email for faster reads (duplication allowed).

---

### 7) Indexing (Often Forgotten)

**Why it matters:**  
Indexes speed reads but slow writes.

**Guideline:**  
Index only on fields used in frequent queries.

---

### 8) Partitioning vs Sharding (Quick Distinction)

- **Partitioning:** split data within a DB (logical separation).
- **Sharding:** split data across DB nodes (physical separation).

**Interview line:**  
“Partitioning is inside a database; sharding is across databases.”

---

### 9) Consistency Models (Tie to DB Choice)

- **Strong consistency:** required for money, inventory, auth
- **Eventual consistency:** ok for feeds, likes, counters

**Interview line:**  
“If correctness is critical, I choose strong consistency even if latency is higher.”

---

### 10) Real-World Examples

- **Orders/Payments:** SQL (transactions, consistency)
- **Feed/Timeline:** NoSQL (high throughput)
- **Session Store:** NoSQL (Redis)

---

### 11) Trade-offs (Say This Explicitly)

- **SQL:** better correctness, harder scale  
- **NoSQL:** better scale, weaker consistency

**Interview line:**  
“I’d pick SQL for transactions, and NoSQL for scale-heavy read/write workloads.”

---

### 12) Failure & Migration Considerations

- **Backups + restore plan**
- **Schema migrations** (SQL)
- **Multi-region replication** (if required)

---

### 13) Quick Practice Prompts (Self-Test)

1. When would you pick SQL over NoSQL?
2. What’s the downside of denormalization?
3. How do indexes affect writes?
4. What’s the difference between partitioning and sharding?
5. When is eventual consistency acceptable?

---

### 14) Quick Answers

1. **SQL vs NoSQL:**  
   SQL for transactions and complex queries; NoSQL for scale and flexible schema.

2. **Denormalization downside:**  
   Data duplication and harder writes/updates.

3. **Indexes vs writes:**  
   Indexes speed reads but slow writes (more maintenance).

4. **Partitioning vs sharding:**  
   Partitioning is within a DB; sharding is across DB nodes.

5. **Eventual consistency:**  
   Acceptable for feeds, likes, counters, and non-critical data.

---

### 15) 20-Second High-Signal Answer (Practice)

“I start with access patterns and consistency requirements. For transactional systems like orders/payments, I’d choose SQL for ACID guarantees and strong correctness. For scale-heavy reads/writes like feeds, I’d use NoSQL and denormalize for speed. I’d add indexes for hot queries and shard once a single node becomes a bottleneck.”
