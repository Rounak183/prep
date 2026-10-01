# Mental Blocks — URL Shortening

Reusable mental checklist for a system design round, using URL shortening as the worked example.

## 1. What, Why

- What is the system, why does it exist (motivation, similar services).

## 2. Requirements

### 2.1 Functional
- Redirection (short URL → long URL).
- Custom alias.
- Expiration time.
- Shorter unique alias is generated automatically.

### 2.2 Non-functional
- Highly available.
- Minimal latency.
- Non-guessable (short links shouldn't be predictable).

### 2.3 Extended
- REST APIs accessible.
- Analytics.

## 3. Capacity Estimates

- QPS.
- Read/Write ratio.
- Storage.
- Bandwidth.
- Network.
- Traffic estimates.
- Roll up into a high-level estimates table.

## 4. Database Design

- Discuss SQL vs. NoSQL — what's actually needed here (simple key-value lookup, high read volume, no complex joins → NoSQL fits well).

## 5. System APIs

- Create.
- Delete.
- Rate-limiting based on API key.

## 6. Basic System Design and Algorithm

### 6.1 Encoding the actual URL
- MD5 → 128-bit hash → 21 characters.
- Choose 6 characters.
- Auto-incrementing sequence.
  - problem is overflow of this integer
- Append user ID.
- Swap characters to avoid duplication.

### 6.2 Key Generation Service (KGS)
- 6-character auto-generated keys.
- Standby server for availability.
- Some keys cached for quick access.

### 6.3 Other constraints
- Impose a limit on alias length.
- Consider size of KGS.

## 7. Data Partitioning and Replication

- What is partitioning.
- Range-based partitioning.
- Hash-based partitioning.
  - Use consistent hashing.
    - Explain what consistent hashing is:
      - Servers and keys are both hashed onto the same circular ring (0 to 2^32-1).
      - A key belongs to the first server found going clockwise from its position on the ring.
      - Adding/removing a server only remaps the keys between it and its predecessor — not the whole keyspace.
      - Solves the "rehash everything" problem of plain `hash(key) % N` when N changes.
      - Virtual nodes: each physical server gets multiple points on the ring, so load spreads evenly and no single server gets a disproportionate range.

## 8. Cache

- Use an off-the-shelf option like Memcache.
- Size of Memcache.
- Use 1–2 servers.
- Cache eviction policy — LinkedHashMap / LRU.
  - Explain how LinkedHashMap implements LRU.
- Replicate cache servers to distribute load between them.

## 9. Load Balancers

- Placement: clients ↔ app servers, app servers ↔ DBs, app servers ↔ cache servers.
- Round robin.
  - Takes out any server that is dead.
- Round robin doesn't factor in load — a server can be overloaded or slow and still get traffic.
- Need a more intelligent LB that queries backend servers about their load and adjusts traffic accordingly.

## 10. Purging / DB Cleanup

- Approach 1 — lazy cleanup: return an error when a user tries to access an expired link.
- Separate cleanup service that runs periodically to remove expired links from DB and cache; scheduled to run only when load is low.
- Default expiration time for each link.
- Put the key back into the KGS key pool.
- Don't bother removing unused keys — storage is cheap.

## 11. Telemetry

- Separate DB for tracking requests made on a URL.
- Show it via a Grafana dashboard.
- Custom wrapper around APIs to track usage — a `usage_analytics` wrapper.
- Wrapper tracks: country, date, time, browser, platform, webpage.
- Separate DB for telemetry is generally the right call, not overkill:
  - Analytics writes are high-volume, append-only, don't need strong consistency — mixing into the main URL-mapping DB competes for I/O and can slow redirects (the latency-critical path).
  - Analytics queries (aggregations, time-series, dashboards) have a different access pattern than "look up one key" — a columnar/time-series store (e.g. Cassandra, ClickHouse) fits better than the KV store backing redirects.
  - Isolates blast radius: a runaway analytics query or write spike can't degrade the core redirect service.
  - Don't write to the telemetry DB synchronously on the request path — queue it (Kafka/SQS) and write asynchronously, so a slow analytics DB never adds latency to a redirect.

## 12. Security and Permissions

- Public/Private flag on each URL in the DB.
- Separate DB storing user IDs and which URLs they're allowed to see.
- No access → return 401.
- Can use Cassandra for this: partition key = hash/KGS key, columns = user IDs with permission to access the URL.
