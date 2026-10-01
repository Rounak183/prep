# Mental Blocks — Pastebin

Reusable mental checklist for a system design round, using Pastebin as the worked example. Shares a lot with URL Shortening — see `url_shortener_summary.md` for shared sections.

## 1. What, Why

- Store plain text (or images), get a unique URL back to access it.
- Used to share text/logs/code quickly by just passing a link.

## 2. Requirements

### 2.1 Functional
- Upload/paste data, get a unique URL back.
- Text only (no other file types).
- Data + link auto-expire after a timespan; user can also set custom expiration.
- Optional custom alias for the paste.

### 2.2 Non-functional
- Highly reliable — uploaded data should never be lost.
- Highly available.
- Real-time access, minimum latency.
- Links non-guessable.

### 2.3 Extended
- Analytics (e.g. how many times a paste was accessed).
- Accessible via REST APIs.

## 3. Design Considerations (Pastebin-specific)

- Limit paste size — e.g. cap at 10MB to prevent abuse.
- Impose a size limit on custom URLs too, to keep the URL DB consistent.

## 4. Capacity Estimates

- Read-heavy — assume 5:1 read/write ratio.
- 1M new pastes/day → ~12 writes/sec; 5M reads/day → ~58 reads/sec.
- Storage: avg paste ~10KB → 10GB/day → ~36TB over 10 years (3.6B pastes); with 70% capacity buffer → ~51.4TB.
- Keys: 6-char base64 → 64^6 ≈ 68.7B unique keys, way more than the 3.6B needed; storing all keys ≈ 22GB (negligible vs. 36TB).
- Bandwidth: ~120KB/s ingress, ~0.6MB/s egress.
- Cache: 80/20 rule → cache top 20% of reads ≈ 10GB.

## 5. System APIs

- Create: `api_dev_key`, `paste_data`, `custom_url` (optional), `user_name` (optional), `paste_name` (optional), `expire_date` (optional) → returns URL or error.
- Retrieve: `api_paste_key` → returns paste contents.
- Delete: `api_dev_key`, `api_paste_key` → returns true/false.

## 6. Database Design

- Billions of records, but metadata per paste is tiny (<100 bytes); paste content itself can be MBs.
- No real relationships between records (except optionally user → paste).
- Read-heavy workload.
- Two tables: Paste metadata (URLHash, ContentKey, expiry, etc.) and Users.

## 7. High-Level Design

- Application layer handles reads/writes.
- Split storage layer in two so each scales independently:
  - Metadata DB (paste info, user info).
  - Object storage for actual paste content (e.g. S3).

## 8. Component Design

### 8.1 Write path
- Generate a random 6-char key (or use user's custom alias).
- Store paste content + key in DB; return key/URL to user.
- Handle key collisions: retry generation, or reject if custom alias already exists.
- Better: standalone Key Generation Service (KGS) — pre-generates unique keys into a key-DB (unused vs. used tables), app servers just pull from it.
  - KGS caches some keys in memory for speed; if KGS dies mid-batch those cached keys are wasted (acceptable — huge key space).
  - KGS is a SPOF → run a standby replica.
  - App servers can also cache keys locally, same trade-off (lose a few keys if the app server dies, but fine given key space size).

### 8.2 Read path
- App layer looks up the key in metadata DB; if found, fetch content from object storage and return it; else return an error.

### 8.3 Datastore layer
- Metadata DB: relational (MySQL) or distributed KV (Dynamo/Cassandra).
- Object storage: S3-like, scales horizontally by adding more servers.

## 9. Shared with URL Shortening

- Purging / DB cleanup.
- Data partitioning and replication (consistent hashing, etc.).
- Cache and load balancer.
- Security and permissions.

(See `url_shortener_summary.md` sections 7–12 for the full detail on each of these.)
