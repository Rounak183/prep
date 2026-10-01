# Mental Blocks — Dropbox

Reusable mental checklist for a system design round, using a file hosting/sync service (Dropbox/Google Drive) as the worked example.

## 1. What, Why

- Cloud file storage — store data on remote servers, access it from any device.
- Value props: availability (anywhere/anytime), reliability/durability (multiple geo-replicated copies), scalability (pay for as much storage as you want).

## 2. Requirements

### 2.1 Functional
- Upload/download files from any device.
- Share files/folders with other users.
- Automatic sync across devices — edit on one, propagate to all.
- Support large files, up to a GB.
- ACID guarantees on file operations.
- Offline editing — add/delete/modify offline, sync once back online.

### 2.2 Extended
- Snapshotting — ability to roll back to any past version of a file.

## 3. Design Considerations

- Expect huge read and write volumes, roughly equal read:write ratio.
- Store files as chunks (e.g. 4MB) — retry only the failed chunk, not the whole file.
- Transfer only updated chunks, not the whole file, to cut bandwidth.
- Deduplicate identical chunks to save storage + bandwidth.
- Keep a local copy of metadata on the client — saves round trips to the server.
- For small edits, upload diffs instead of a whole chunk.

## 4. Capacity Estimates

- 500M total users, 100M DAU, ~3 devices/user.
- ~200 files/user → 100B total files.
- Avg file size 100KB → ~10PB total storage.
- ~1M active connections/minute.

## 5. High-Level Design

- User designates a local workspace folder; anything placed in it syncs to the cloud and out to the user's other devices.
- Three server roles:
  - Block servers — upload/download files to/from Cloud Storage.
  - Metadata servers — keep file/user metadata in SQL or NoSQL.
  - Synchronization servers — notify all clients of changes so they can sync.

## 6. Component Design

### 6.1 Client
- Core jobs: upload/download files, detect local file changes, handle conflicts from offline/concurrent edits.
- Chunking: split files into fixed-size chunks (e.g. 4MB); only transfer chunks that changed. Optimal chunk size depends on storage IOPS, network bandwidth, and average file size.
- Metadata records which chunks make up each file.
- Local metadata copy enables offline edits and cuts round trips.
- Listening for remote changes: periodic polling wastes bandwidth and adds delay → use HTTP long polling instead (server holds the request open until there's new data, then responds; client immediately re-polls).
- Client is split into four parts:
  - Internal Metadata DB — tracks files, chunks, versions, locations.
  - Chunker — splits files into chunks, reconstructs files from chunks, detects modified parts to avoid re-transferring unchanged ones.
  - Watcher — monitors the local workspace for user actions (create/delete/update) and also listens for remote changes broadcast by the Synchronization Service.
  - Indexer — consumes Watcher events, updates internal metadata DB, and once chunks are uploaded/downloaded, tells the Synchronization Service to broadcast the change and update remote metadata.
- Slow server handling: client should exponentially back off retries.
- Mobile clients sync on demand rather than immediately, to save bandwidth/space.

### 6.2 Metadata Database
- Tracks versioning + metadata for files/chunks, users, devices, workspaces.
- Relational (MySQL) or NoSQL (DynamoDB).
- Relational DB gives ACID natively; with NoSQL, ACID has to be built into the Synchronization Service's logic instead.
- Stores: Chunks, Files, Users, Devices, Workspaces (sync folders).

### 6.3 Synchronization Service
- Applies a client's file update and pushes it out to other subscribed clients; also reconciles clients' local DB with the remote Metadata DB.
- Offline client polls for updates once it reconnects.
- On update: validate against Metadata DB, apply update, notify subscribed users/devices.
- Minimizes data moved via a differencing algorithm — transmit only the changed chunk(s), not the whole file.
- Uses chunk hashes (e.g. SHA-256) to decide whether the client's local copy needs updating, and to detect duplicate chunks server-side (see deduplication below).
- Sits behind a messaging middleware so multiple Synchronization Service instances can pull from a shared request queue and load-balance the work.

### 6.4 Message Queuing Service
- Async, loosely-coupled messaging between clients and the Synchronization Service.
- Request Queue — one global queue shared by all clients; updates flow here first, Synchronization Service consumes it.
- Response Queues — one per subscribed client, since a delivered message is removed from the queue and each client needs its own copy of pending updates.

### 6.5 Cloud/Block Storage
- Stores the actual file chunks; clients talk to it directly for upload/download.
- Kept separate from metadata so storage can be swapped (cloud or in-house) independently.

## 7. File Processing Workflow

- Client A uploads chunks to cloud storage.
- Client A updates metadata, commits changes.
- Client A gets confirmation; Clients B and C (file is shared with them) get notified.
- B and C receive the metadata change and pull the updated chunks.
- If B/C are offline, the Message Queuing Service holds their update in their Response Queue until they reconnect.

## 8. Data Deduplication

- Hash each incoming chunk, compare against existing chunk hashes to avoid storing/transferring duplicates.
- Post-process dedup: store first, dedup later in the background.
  - No write-path latency hit, but briefly stores duplicate data and still burns bandwidth transferring it.
- In-line dedup: hash and check in real time as data comes in.
  - If a matching chunk already exists, store just a metadata reference instead of the data — best network + storage efficiency, at the cost of write-path latency for the hash lookup.

## 9. Metadata Partitioning

- Vertical partitioning: split tables by feature (e.g. users DB vs. files/chunks DB).
  - Simple, but doesn't solve scale within a single huge table, and cross-DB joins hurt performance/consistency.
- Range-based partitioning: e.g. shard files by first letter of file path.
  - Predictable placement, but prone to unbalanced partitions (e.g. one letter gets disproportionately more files).
- Hash-based partitioning: hash FileID → partition number (e.g. into 1...256 buckets).
  - Distributes more evenly, but can still create hot partitions — fix with consistent hashing.

## 10. Cache

- Block storage cache: off-the-shelf (Memcached), keyed by chunk ID/hash, checked before hitting Block storage. Size cache servers off usage patterns (e.g. a 144GB server can hold ~36K chunks).
- Eviction policy: LRU — discard least recently used chunk when full.
- Also cache the Metadata DB similarly.

## 11. Load Balancer

- Two LB points: clients ↔ Block servers, clients ↔ Metadata servers.
- Start with Round Robin — simple, evenly distributes load, drops dead servers from rotation.
- Round Robin doesn't account for load — need a smarter LB that queries backend load and routes accordingly.

## 12. Security, Permissions and File Sharing

- Store per-file permissions in the metadata DB — controls who can view/modify a file, including shared and public files.
