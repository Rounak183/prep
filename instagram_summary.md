# Mental Blocks — Instagram

Reusable mental checklist for a system design round, using a photo-sharing service like Instagram as the worked example.

## 1. What, Why

- Photo-sharing social network: users upload/share photos and videos, publicly or privately.
- Simplified scope: users upload photos, follow other users, News Feed = top photos from people they follow.
- Similar services: Flickr, Picasa.

## 2. Requirements

### 2.1 Functional
- Upload/download/view photos.
- Search based on photo/video titles.
- Follow other users.
- Generate and display a News Feed of top photos from followed users.

### 2.2 Non-functional
- Highly available.
- News Feed generation latency ≤ 200ms.
- Can trade consistency for availability (fine if a photo doesn't show up for a while).
- Highly reliable — an uploaded photo/video should never be lost.

### 2.3 Out of scope
- Tags on photos, tag search, comments, tagging users, "who to follow" suggestions.

## 3. Design Considerations

- Read-heavy system → optimize for fast retrieval.
- Users can upload unlimited photos → storage management is critical.
- Low latency expected on viewing photos.
- Data must be 100% reliable — no photo loss.

## 4. Capacity Estimates

- 500M total users, 1M daily active users.
- 2M new photos/day → ~23 photos/sec.
- Avg photo size: 200KB.
- Storage: 1 day ≈ 400GB (2M × 200KB); 10 years ≈ 1425TB.
- Roll up into a high-level estimates table.

## 5. High Level System Design

- Two flows: upload photos, and view/search photos.
- Need object storage servers (photos) + database servers (metadata).

## 6. Database Schema

- Discuss SQL vs. NoSQL — need joins (User, Photo, follow relationships) which pulls toward RDBMS (MySQL), but NoSQL scales better for this read-heavy, high-volume case.
- Tables: User, Photo, UserPhoto, UserFollow.
- Index on (PhotoID, CreationDate) — need to fetch recent photos first.
- Photos themselves → distributed file storage (HDFS/S3).
- Metadata → distributed key-value store: key = PhotoID, value = object with PhotoLocation, UserLocation, CreationTimestamp, etc.
- UserPhoto / UserFollow → wide-column store (Cassandra): key = UserID, value = list of PhotoIDs (or followed UserIDs) across columns.
- Cassandra-style stores maintain replicas for reliability; deletes aren't instant — retained for some days before permanent removal (undelete support).

## 7. Data Size Estimation

- User row ≈ 68 bytes (UserID, Name, Email, DateOfBirth, CreationDate, LastLogin) → 500M users ≈ 32GB.
- Photo row ≈ 284 bytes (PhotoID, UserID, PhotoPath, lat/long × 2, CreationDate) → 2M/day ≈ 0.5GB/day → 1.88TB over 10 years.
- UserFollow row ≈ 8 bytes; 500M users × 500 avg follows ≈ 1.82TB.
- Total ≈ 3.7TB over 10 years.

## 8. Component Design

- Uploads (writes) are slow (disk-bound); reads are fast, especially from cache.
- Web servers have a connection limit (e.g. 500) — uploads can hog all connections and starve reads.
- Fix: split into separate read servers and write servers so uploads don't block reads.
- Separating reads/writes also lets each path scale and optimize independently.

## 9. Reliability and Redundancy

- Store multiple copies of every file — if one storage server dies, retrieve from another copy.
- Same principle for other components: run multiple replicas of every service so partial failure doesn't take down the system.
- Redundancy removes single points of failure.
- Even single-instance services should have a standby/secondary that takes over on failover (automatic or manual).

## 10. Data Sharding

### 10.1 Partition by UserID
- Keeps all of a user's photos on the same shard.
- Shard = UserID % N (e.g. 10 shards for 3.7TB / 1TB-per-shard).
- Append ShardID to PhotoID for global uniqueness; each shard can auto-increment its own PhotoID.
- Problems:
  - Hot users (celebrities) create hotspots — disproportionate read load on one shard.
  - Non-uniform storage distribution (some users have far more photos).
  - Can't split one user's photos across shards without adding latency.
  - Shard outage takes out all of that user's data.

### 10.2 Partition by PhotoID
- Generate a globally unique PhotoID first, then shard = PhotoID % N — solves the hot-user/uniform-distribution problem.
- No need to append ShardID since PhotoID is already unique.
- Can't auto-increment per shard anymore (need the ID before knowing the shard) — need a separate ID-generation mechanism:
  - Dedicated DB instance(s) generating auto-incrementing IDs (a table with just a 64-bit ID column).
  - Single point of failure risk → run two ID generators, one even, one odd, behind a load balancer round-robining between them.
  - Alternative: reuse the Key Generation Service pattern from URL shortening.
- Planning for growth: define many logical partitions up front, multiple logical partitions per physical server initially; migrate logical partitions to new servers as load grows. Maintain a config file/DB mapping logical partitions → physical servers so moves only require a config update.

## 11. Ranking and News Feed Generation

- Naive approach: fetch list of followed users, pull latest ~100 photos from each, run ranking (recency, likeness, etc.) at read time — high latency due to querying many tables + sort/merge/rank.
- Better: pre-generate News Feed into a dedicated `UserNewsFeed` table via background servers; on request, just read from this table.
- Feed-generation servers check `UserNewsFeed` for the last generation timestamp and generate incrementally from there.
- Delivery models:
  - Pull: client polls periodically/manually — can show stale data, and most polls return empty.
  - Push: server pushes updates immediately (long-poll) — breaks down for celebrity users with millions of followers (too many pushes).
  - Hybrid: push to users with few follows/followers, fall back to pull for high-fanout users; or cap push frequency globally and let heavy users pull.

## 12. News Feed Creation with Sharded Data

- Need to sort photos by creation time efficiently → encode creation time into the PhotoID itself.
- PhotoID = epoch timestamp (high bits) + auto-incrementing sequence (low bits); primary index on PhotoID makes "latest photos" queries fast.
- Shard = PhotoID % N, same as before.
- Sizing: ~1.6 billion seconds over 50 years → 31 bits for the timestamp; ~23 photos/sec → 9 bits for the sequence (2^9 = 512 photos/sec capacity), sequence resets every second.
- Total PhotoID size = 31 + 9 = 40 bits (fits comfortably within a 64-bit ID).

## 13. Cache and Load Balancing

- Need a massive-scale, geographically distributed photo delivery system — CDN + distributed photo cache servers close to users.
- Separate metadata cache (Memcache) in front of the DB for hot rows; app servers check cache before hitting DB.
- Eviction policy: LRU (discard least-recently-viewed row first).
- 80/20 rule: ~20% of daily photo reads drive ~80% of traffic → cache that hot 20% of photos and metadata rather than trying to cache everything.
