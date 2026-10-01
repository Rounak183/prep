# Mental Blocks — Facebook Messenger

Reusable mental checklist for a system design round, using an instant messaging service (Facebook Messenger) as the worked example.

## 1. What, Why

- Text-based instant messaging, web + mobile, between Facebook friends.

## 2. Requirements

### 2.1 Functional
- One-on-one conversations between users.
- Track online/offline status of users.
- Persistent storage of chat history.

### 2.2 Non-functional
- Real-time chat, minimum latency.
- Highly consistent — same chat history across all of a user's devices.
- High availability desirable, but consistency wins over availability if we have to trade off.

### 2.3 Extended
- Group chats.
- Push notifications for offline users.

## 3. Capacity Estimates

- 500M DAU, 40 msgs/user/day → 20B messages/day.
- Storage: ~100 bytes/msg → 2TB/day → ~3.6PB for 5 years (ignoring compression/replication).
- Bandwidth: 2TB/day → ~25MB/s incoming, same ~25MB/s outgoing (every message goes to someone else too).

## 4. High-Level Design

- Central chat server orchestrates communication.
- Flow: A sends msg → server ACKs A → server stores msg + forwards to B → B ACKs server → server tells A it was delivered.

## 5. Detailed Component Design

### 5.1 Message handling
- Pull model (client polls for new messages) vs. push model (client keeps connection open, server pushes) — push wins, avoids wasted empty-poll requests and cuts latency.
- Maintain open connection via long polling or WebSockets.
  - Long polling: client requests, server holds the request open until there's data (or timeout), then responds; client immediately re-requests.
- Server tracks connections in a hash table: UserID → connection object. Look up receiver's connection to deliver.
- Receiver offline when message arrives:
  - Permanent/long disconnect → notify sender of delivery failure.
  - Temporary disconnect (e.g. long-poll timeout) → expect reconnect, ask sender to retry (can be automatic in client logic); server can also hold the message briefly and retry once receiver reconnects.
- Sizing: plan for 500M concurrent connections; ~50K connections/server → ~10K chat servers needed.
- Use a load balancer in front of chat servers to map UserID → the server holding that user's connection.
- Handling a "deliver message" request: store in DB, send to receiver, ACK sender — don't block the ACK on the DB write (do that async/in background).
- Message ordering: server-receipt timestamp alone isn't enough (two messages crossing in flight can look reordered to each client). Use a per-user sequence number instead — each client's message stream stays internally consistent even though the two users' views of ordering differ from each other.

### 5.2 Storing and retrieving messages
- Options to persist: separate writer thread, or async write request to DB.
- Things to handle: DB connection pool efficiency, retrying failed writes, logging requests that fail even after retries, and replaying those once the underlying issue is fixed.
- Storage engine: need high-rate small writes + fast sequential range reads → rules out plain RDBMS/MongoDB-style row read/write per message.
  - Wide-column store like HBase fits: buffers writes in memory, flushes to disk, good at storing/fetching variable-size rows by key or range-scanning them (HDFS-backed, modeled on BigTable).
- Clients paginate when fetching history; page size can vary by device (e.g. smaller for phones).

### 5.3 Managing online/offline status
- Connection object per active user already tells us who's online.
- Broadcasting every status change to everyone is expensive at 500M concurrent users — optimizations:
  - Client pulls friends' current status on app start.
  - Message to an offline user → fail to sender + update that user's status on the client.
  - Coming online → broadcast after a short delay (avoid noise from users who reconnect immediately).
  - Clients pull status only for users visible in their current viewport, and not too frequently — stale offline status is acceptable for a while.
  - Pull status when starting a new chat with someone.

### 5.4 Design summary
- Clients hold an open connection to the chat server; server pushes messages over it via long poll.
- Messages persisted in HBase (fast small writes + range scans).
- Online status broadcast to relevant users; offline/viewport status pulled by clients less frequently.

## 6. Data Partitioning

- ~3.6PB over 5 years → must shard across many DB servers.
- Partition by hash(UserID) % N — keeps one user's full message history on one shard, and makes history fetches fast.
  - ~900 shards needed at 4TB/shard; round to 1000 for simplicity.
  - Start with more logical partitions than physical servers, multiple shards per server, and split out onto more servers as storage demand grows.
- Don't partition by MessageID — scattering one user's messages across shards makes range fetches (chat history) slow.

## 7. Cache

- Cache last ~15 messages of the last ~5 conversations visible in a user's viewport.
- Since a user's messages all live on one shard, that user's cache also lives entirely on one machine.

## 8. Load Balancing

- LB in front of chat servers: maps UserID → the server holding that user's connection.
- Separate LB needed for cache servers too.

## 9. Fault Tolerance and Replication

- Chat server dies: TCP connections can't really be failed-over — simplest fix is client auto-reconnect logic.
- Never keep only one copy of a user's messages — replicate across servers (or use erasure coding like Reed-Solomon) so a server crash doesn't lose data permanently.

## 10. Extended Requirements

### 10.1 Group chat
- Separate group-chat object identified by GroupChatID, holding the list of participants.
- LB routes group messages by GroupChatID; the server handling that group chat fans the message out to each participant's connection-holding server.
- Store group chats in a separate table partitioned by GroupChatID.

### 10.2 Push notifications
- Needed because offline users currently just get a failure sent to the sender.
- Users opt in per device/browser.
- Add a Notification server: takes messages meant for offline users and forwards them to the manufacturer's push notification service (APNs/FCM-style), which delivers to the device.
