# Mental Blocks — Twitter

Reusable mental checklist for a system design round, using a social networking / microblogging service (Twitter) as the worked example.

## 1. What, Why

- Post/read short (140-char) messages ("tweets"). Registered users post+read, unregistered can only read.
- Access via website, SMS, or mobile app.

## 2. Requirements

### 2.1 Functional
- Post new tweets.
- Follow other users.
- Mark tweets as favorites.
- Generate/display a timeline of top tweets from followed users.
- Tweets can contain photos and videos.

### 2.2 Non-functional
- Highly available.
- Timeline generation latency ≤ 200ms.
- Consistency can take a hit for availability — fine if a tweet doesn't show up for a while.

### 2.3 Extended
- Search for tweets.
- Reply to a tweet.
- Trending topics.
- Tagging other users.
- Tweet notifications.
- "Who to follow" suggestions.
- Moments.

## 3. Capacity Estimates

- 1B total users, 200M DAU, avg 200 follows/user.
- Favorites: 200M × 5/day = 1B favorites/day.
- Tweet-views: DAU × ((2 own-timeline visits + 5 other-page visits) × 20 tweets/page) ≈ 28B views/day.
- Storage: 100M new tweets/day × (280 bytes text + 30 bytes metadata) ≈ 30GB/day (text only).
- Media: ~1/5 tweets have a photo (200KB), ~1/10 have a video (2MB) → ~24TB/day of new media.
- Bandwidth: ingress ~290MB/s (media). Egress ~35GB/s total — text ~93MB/s, photos ~13GB/s (show every photo), videos ~22GB/s (assume only every 3rd video watched).
- Writes ≈ 1150 tweets/sec avg; reads ≈ 325K/sec avg — strongly read-heavy. Expect multi-thousand write and ~1M read peaks.

## 4. System APIs

- Post tweet: `api_dev_key`, `tweet_data`, `tweet_location` (optional), `user_location` (optional), `media_ids` (optional, uploaded separately) → returns tweet URL or error.

## 5. High-Level Design

- Multiple app servers behind load balancers.
- DB layer needs to handle huge read volume + steady write volume.
- Separate file storage for photos/videos.

## 6. Database Schema

- Need: Users, Tweets, Favorites, Follows.
- SQL vs NoSQL trade-off — same discussion as Instagram's database schema section.

## 7. Data Sharding

### 7.1 By UserID
- Hash UserID → server; keeps a user's tweets/favorites/follows together, fast to query per-user.
- Problems: hot users overload their shard; uneven data growth across users. Fix with repartitioning or consistent hashing.

### 7.2 By TweetID
- Hash TweetID → random server. Timeline generation: find followees → query all DB servers for their tweets → each server sorts+returns top tweets → app server merges/sorts again.
- Solves hot-user problem, but every timeline request now fans out to all shards → higher latency. Mitigate with a cache for hot tweets.

### 7.3 By tweet creation time
- Store by time → fetching "latest" is fast, only a few servers queried.
- Problem: all new writes hit one server (today's), old servers idle; that same server also takes disproportionate read load.

### 7.4 Combine TweetID + creation time (the actual approach)
- Encode creation time inside the TweetID itself instead of storing it separately, then shard by TweetID → get fast "latest tweets" queries *and* even write/read distribution.
- TweetID = epoch seconds (31 bits, covers next 50 years) + auto-incrementing sequence (17 bits → 130K tweets/sec capacity, resets every second) = 48 bits; can round up to 64 bits for 100-year/ms-granularity headroom.
- Two ID-generator DBs (even/odd) for fault tolerance, same pattern as Instagram's PhotoID generation.
- Still queries all shards for timeline generation, but reads/writes themselves are faster: no secondary index on creation time needed (it's baked into the primary key).

## 8. Cache

- Memcache-style cache in front of DB for hot tweets/users; check cache before DB.
- Eviction: LRU.
- 80/20 rule: cache ~20% of daily read volume per shard (the popular tweets).
- Recency-based caching: if ~80% of users only see the last 3 days of tweets, cache all tweets from the last 3 days (~100GB at 30GB/day text-only) — fits on one server, but replicate across several to spread read load.
- Cache structure: hash table keyed by OwnerID → doubly linked list of that user's tweets from the last 3 days; insert new tweets at the head, evict from the tail (oldest) when space is needed.
- Same recency-caching idea extends to photos/videos from the last 3 days.

## 9. Timeline Generation

- Covered in depth under Facebook Newsfeed / Instagram's ranking section — pre-generate into a per-user table, pull vs push vs hybrid delivery.

## 10. Replication and Fault Tolerance

- Read-heavy → multiple secondary DB replicas per shard, serving reads only.
- Writes go to primary first, then replicate to secondaries.
- Also gives failover: promote a secondary if the primary goes down.

## 11. Load Balancing

- Three LB points: clients ↔ app servers, app servers ↔ DB replicas, aggregation servers ↔ cache servers.
- Start with Round Robin (simple, drops dead servers); upgrade to a load-aware LB that queries backend load and adjusts routing, since Round Robin ignores overload/slowness.

## 12. Monitoring

- Track: new tweets/day/sec (and peak), timeline delivery volume/rate, average timeline-refresh latency.
- These signals tell you when you need more replication, load balancing, or caching.

## 13. Extended Requirements

- Feed serving: fetch latest tweets from followees, merge/sort by time, paginate; top-N depends on client viewport (mobile shows fewer than web); can pre-cache the next page.
- Retweet: store just the original TweetID reference, no duplicated content.
- Trending topics: cache most frequent hashtags/queries over a recent window, refresh periodically; rank by tweet/search/retweet/like frequency, weight by reach.
- Who to follow: suggest friends-of-follows (2-3 hops out), bias toward people with more followers; use ML to re-rank (recent follow-growth, mutual follows, location/interest overlap) since only a few suggestions can be shown at once.
- Moments: pull top news from recent hours, find related tweets, cluster/categorize via ML (news, sports, entertainment, etc.), surface as trending Moments.
- Search: indexing + ranking + retrieval — see Twitter Search as its own design.
