# Facebook Messenger System Design - Detailed Example

This document walks through designing an instant messaging service like Facebook Messenger. Use `SYSTEM_DESIGN_TEMPLATE.md` for the full 8-step framework; this file captures requirements, capacity math, and the core design decisions for real-time chat.

**Difficulty Level:** Medium  
**Similar services:** WhatsApp, iMessage, Telegram, Slack DMs

---

## Step 1: Problem Understanding & Requirements Clarification

### 1.1 Problem Statement

Design an instant messaging service where users send text messages to each other through web and mobile clients.

**What is Facebook Messenger?**  
Facebook Messenger is a software application that provides text-based instant messaging. Users chat with Facebook friends from cell phones and from Facebook's website.

### 1.2 Functional Requirements

1. **One-on-one chat:** Support direct conversations between two users.
2. **Presence:** Track and expose online/offline (and optionally idle) status.
3. **Persistent history:** Store chat history so users can scroll back and sync across devices.

### 1.3 Non-Functional Requirements

1. **Low latency:** Real-time delivery; target end-to-end latency in the low hundreds of ms for online users.
2. **Strong consistency for history:** Same chat history on phone, web, and tablet (prefer CP over AP when forced to choose).
3. **High availability:** Desirable, but we can trade some availability for consistency (e.g., fail closed on write rather than show divergent history).

### 1.4 Extended Requirements (Optional)

1. **Group chats:** Multiple participants in one conversation.
2. **Push notifications:** Notify offline users of new messages (APNs, FCM, web push).
3. **Media messages:** Images, video, voice notes (often offloaded to object storage + CDN).
4. **Read receipts / typing indicators:** Ephemeral signals, not part of durable history.

### 1.5 Clarifying Questions (Interview)

| Topic | Typical assumption |
|-------|-------------------|
| Message types | Text only for MVP; media as extension |
| Max group size | 256 or 500 members |
| Message retention | Forever unless user deletes; legal hold as separate concern |
| Ordering | Per-conversation total order via server-assigned sequence or timestamp + tie-break |
| Friends graph | Reuse Facebook social graph; only friends can message (or open DMs) |

---

## Step 2: Capacity Estimation (BTSM Framework)

### 2.1 Assumptions

| Assumption | Value |
|------------|-------|
| Daily active users (DAU) | 500 million |
| Messages per user per day | 40 |
| Total messages per day | 20 billion |
| Average message body size | 100 bytes (text only) |
| Chat history retention | 5 years |
| Read/write ratio | ~1:1 for active chats (each send → one receive); history sync adds read load |

### 2.2 Traffic Estimation

**Messages per second (write QPS):**
```
20,000,000,000 / 86,400 ≈ 231,000 messages/s
Round for interviews: ~230K writes/s
```

**Read QPS (rough):**
- Opening a thread: fetch last N messages (pagination).
- Assume 2× write traffic from history loads, presence polls, and sync: **~460K reads/s** (order-of-magnitude).

**Peak multiplier:** Plan for **2–3×** average → **~500K–700K msg/s** at peak.

### 2.3 Storage Estimation

**Daily message payload:**
```
20B messages × 100 bytes = 2 TB/day (payload only)
```

**Five years of message bodies:**
```
2 TB/day × 365 days × 5 years ≈ 3.6 PB
```

**Metadata overhead (per message):**  
message_id, conversation_id, sender_id, timestamp, indexes → often **2–5×** payload size in practice.

| Component | Rough size |
|-----------|------------|
| Message bodies (5 yr) | ~3.6 PB |
| Metadata + indexes | +50–100% |
| Replication (3×) | ×3 |
| User profiles, conv metadata | Smaller but non-zero |

**Interview number:** **~10–15 PB** replicated over 5 years with metadata and replication (vs 3.6 PB raw text only).

### 2.4 Bandwidth Estimation

**Incoming (writes):**
```
2 TB / 86,400 s ≈ 25 MB/s average
Peak (3×): ~75 MB/s
```

**Outgoing (delivery to recipients):**  
One-to-one: ~1 recipient per message → similar **~25 MB/s** average, **~75 MB/s** peak for fan-out of 1.  
Group chats increase outbound bandwidth (one write, N deliveries).

### 2.5 Memory (Cache) Estimation

**Recent messages per active user:**  
Cache last 50–100 messages per open conversation in Redis (~5–10 KB per active thread).

**Presence:**  
500M DAU × ~50 bytes online record (if all online — unrealistic) → use **active connections** instead:  
50M concurrent WebSockets × 200 bytes ≈ **10 GB** for session routing metadata (sharded).

**Hot users:** 80/20 — cache recent threads for top 20% of users.

### 2.6 Summary Table

| Metric | Value |
|--------|-------|
| Messages/day | 20 billion |
| Write QPS (avg) | ~230K/s |
| Read QPS (avg) | ~460K/s (estimate) |
| Storage (5 yr, text only) | ~3.6 PB |
| Storage (with meta + 3× replication) | ~10–15 PB (planning) |
| Incoming bandwidth (avg) | ~25 MB/s |
| Outgoing bandwidth (avg, 1:1) | ~25 MB/s |
| Concurrent connections (planning\| magnitude) | Tens of millions |

---

## Step 3: System APIs (Draft)

### 3.1 Send Message

`POST /v1/conversations/{conversationId}/messages`

```json
{
  "client_message_id": "uuid-from-client",
  "body": "Hello!",
  "type": "text"
}
```

Response `201`: server `message_id`, `sequence`, `created_at`.

**Idempotency:** `client_message_id` dedupes retries.

### 3.2 Fetch History

`GET /v1/conversations/{conversationId}/messages?before={cursor}&limit=50`

Paginate backward in time (cursor = message_id or sequence).

### 3.3 Real-Time Channel

WebSocket (or long polling fallback):

- Client → server: `send_message`, `typing`, `ack_read`
- Server → client: `new_message`, `presence_update`, `message_delivered`

### 3.4 Presence

`GET /v1/users/{userId}/presence` → `{ "status": "online|offline|away", "last_seen": "..." }`

Updated via WebSocket heartbeat + disconnect events.

---

## Step 4: Database Design (High Level)

### 4.1 Core Entities

**User** — profile, device tokens for push.

**Conversation** — `conversation_id`, type (`direct` | `group`), participant list.

**Message** — `message_id`, `conversation_id`, `sender_id`, `sequence`, `body`, `created_at`.

**UserConversation** — per-user inbox: last message preview, unread count, mute settings (supports sharding by `user_id`).

### 4.2 Storage Choices

| Data | Store | Why |
|------|-------|-----|
| Messages | Cassandra / HBase / custom append log | High write throughput, time-range queries by conversation |
| User / social graph | MySQL / distributed SQL | Strong consistency for identity |
| Presence | Redis | TTL, fast read/write, ephemeral |
| Media | S3 + CDN | Blob storage |
| Push queue | Kafka / SQS | Async notification workers |

### 4.3 Sharding

- **Messages:** partition by `conversation_id` (all messages for a thread co-located).
- **Inbox / UserConversation:** partition by `user_id`.
- **Direct chat lookup:** deterministic `conversation_id = hash(sorted(user_a, user_b))`.

### 4.4 Indexes

- `(conversation_id, sequence DESC)` — history pagination.
- `(user_id, updated_at DESC)` — inbox list.

---

## Step 5: High-Level Design

### 5.1 Core Concept

- **Chat server** is the central piece — orchestrates all communication between users.
- User-A connects to the chat server and sends a message intended for User-B.
- The server:
  - Passes the message to User-B (real-time delivery).
  - Stores the message in the database (persistent history).

### 5.2 System Architecture (Overview)

```
[Mobile/Web Client]
        |
        |  HTTPS (REST: history, upload)
        |  WSS / Long Poll (real-time)
        v
[Load Balancer]
        |
        v
[Chat Server]  ← central orchestrator
        |
        +-----> [Message Database]     (store & retrieve history)
        |
        +-----> [Connection Registry]  (UserID → open connection)
        |
        +-----> [Presence Store]       (online / offline status)
```

### 5.3 End-to-End Message Workflow

1. **Send:** User-A sends a message to User-B through the chat server.
2. **Server ack (sent):** Server receives the message and sends an acknowledgment to User-A.
3. **Persist + deliver:** Server stores the message in the database and sends the message to User-B.
4. **Client ack (received):** User-B receives the message and sends an acknowledgment to the server.
5. **Delivery notification:** Server notifies User-A that the message has been delivered successfully to User-B.

### 5.4 Acknowledgment States (Delivery Pipeline)

| Stage | Who acks | Meaning |
|-------|----------|---------|
| Sent | Server → User-A | Server accepted the message |
| Delivered | User-B → Server → User-A | Message reached User-B's client |
| Read | User-B → Server → User-A | (Extension) User-B opened/read the message |

---

## Step 6: Detailed Component Design

### 6.1 Starting Point — Single Server

- Build a **simple solution first** where everything runs on one server.
- At a high level, the system must handle three use cases:
  - **Receive incoming messages** and **deliver outgoing messages**.
  - **Store and retrieve messages** from the database.
  - **Track online/offline status** of users and **notify relevant users** of status changes.

---

### 6.2 Message Handling

#### 6.2.1 How Users Send and Receive

- **To send:** User connects to the server and posts messages for other users.
- **To receive:** Two architectural options:

**Option A — Pull model**

- Users periodically ask the server if there are any new messages for them.
- Server keeps track of messages **still waiting to be delivered**.
- When the receiving user connects and asks for new messages, server returns all pending messages.
- **Problems:**
  - Users must poll frequently to minimize latency.
  - Most polls return empty — wastes server and network resources.
  - High latency unless polling interval is very short.
  - **Not efficient** for real-time chat.

**Option B — Push model (preferred)**

- Active users keep a **persistent connection open** with the server.
- As soon as the server receives a message, it **immediately passes** it to the intended user.
- Server does **not** need to track pending messages for online users.
- **Minimum latency** — messages delivered instantly on the open connection.
- **Chosen approach** for Messenger-style real-time chat.

#### 6.2.2 Maintaining an Open Connection

- Clients need a long-lived channel to the server.
- Two options:

**HTTP Long Polling**

- Client requests information from the server expecting the server may **not respond immediately**.
- If server has no new data when poll arrives:
  - Does **not** send an empty response.
  - **Holds the request open** until data becomes available.
- Once data is available, server **immediately sends the response**, completing the open request.
- Client **immediately issues another request** for future updates.
- **Benefits:** Improved latency, throughput, and performance vs short polling.
- **Failure cases:**
  - Long poll request **times out** → client opens a new request.
  - Server sends **disconnect** → client opens a new request.

**WebSockets**

- Full-duplex persistent connection (upgrade from HTTP).
- Lower overhead than repeated long polls once established.
- Preferred for modern mobile/web clients when supported.

#### 6.2.3 Tracking Open Connections (Connection Registry)

- Server must efficiently redirect messages to the right user.
- Use a **hash table (in-memory map)**:
  - **Key:** `UserID`
  - **Value:** connection object (socket / long-poll response handle)
- On incoming message for a user:
  1. Look up `UserID` in the hash table.
  2. Find the connection object.
  3. Send the message on the open connection.

#### 6.2.4 Receiver Is Offline

- If receiver has **fully disconnected:**
  - Server can **notify sender about delivery failure** (or mark as pending).
  - Server **stores the message** in the database regardless (history is durable).
- If disconnect is **temporary** (e.g., long-poll timed out, about to reconnect):
  - Expect a **reconnect** from the user shortly.
  - Ask sender to **retry** sending the message.
  - Retry can be **embedded in client logic** — user does not retype the message.
  - Server can **store the message** and **retry delivery** once receiver reconnects.

#### 6.2.5 Message Ordering

- Server assigns monotonic **sequence per conversation** (not client clock).
- Client displays by `sequence`; use `client_message_id` for optimistic UI until ack.

---

### 6.3 Database — Store and Retrieve Messages

- Every message is **persisted before or as part of delivery** (source of truth).
- Supports:
  - Chat history scroll-back on all devices.
  - Delivery to offline users on next sync.
  - Strong consistency requirement across devices.
- Storage choice at scale: Cassandra / HBase (high write throughput, partition by `conversation_id`).
- See Step 4 for schema and sharding details.

---

### 6.4 Presence — Online / Offline Tracking

- Server records which users are **online** vs **offline**.
- On status change, **notify all relevant users** (friends, active chat partners).
- Implementation:
  - Set `UserID` in presence store on connect; remove/TTL on disconnect.
  - Broadcast `presence_update` events over open connections.
- Store: Redis (fast, ephemeral, TTL-based heartbeat).

---

### 6.5 Scaling the Chat Server Tier

#### 6.5.1 Connection Capacity Math

- **Target:** 500 million concurrent connections.
- **Assumption:** One modern server handles ~**50K concurrent connections**.
- **Servers needed:**
  ```
  500,000,000 / 50,000 = 10,000 chat servers
  ```

#### 6.5.2 Multi-Server Considerations (Beyond Single Server)

- **Connection registry** must be **shared or routable** across servers (Redis: `user_id → server_id`).
- **Cross-server message delivery:** pub/sub bus (Redis, Kafka, NATS) so any chat node can reach the connection server holding User-B's socket.
- **Sticky sessions / consistent hashing:** Route a user's connection to the same server when possible.
- **Load balancer** in front of chat server fleet; health checks on connection count.

#### 6.5.3 WebSocket Scaling Summary

- Dedicated **connection tier** separate from REST/history API if needed.
- **Routing:** `user_id → connection server` mapping in Redis.
- **Cross-server delivery:** pub/sub so any chat node can push to any connection node.

---

### 6.6 Group Chat (Extension)

- One `conversation_id`, many participants.
- Write once; fan-out via pub/sub to each member's connection (online via push, offline via push notification).
- For very large groups: consider **fan-out on read** (pull) vs **push to all** (expensive at scale).

---

### 6.7 Push Notifications (Extension — Offline Users)

- Store device tokens per user.
- When receiver has no open connection, enqueue push via FCM / APNs.
- Notification payload: sender, preview, `conversation_id` (not full history).
- Collapse multiple messages: e.g., "3 new messages from Alice".

---

### 6.8 Consistency Across Devices

- All devices read from same message store via `conversation_id + sequence`.
- Read-your-writes: route to same region or linearizable read after write for own messages.

---

## Step 7: Additional Considerations

- **Security:** TLS everywhere; E2E encryption as product extension (key management complexity).
- **Spam / abuse:** rate limits per user, report flow, block list.
- **Deletion:** tombstone messages; GDPR export/delete by user_id.
- **Monitoring:** delivery latency p99, WS connection count, Kafka lag, push success rate.

---

## Step 8: Trade-offs

| Decision | Choice | Trade-off |
|----------|--------|-----------|
| CP vs AP | Favor **consistency** for history | May reject writes or delay during partition |
| WebSocket vs polling | WebSocket primary | Connection state complexity vs latency |
| Fan-out on write vs read | Write fan-out for small groups; read for huge channels | Storage/CPU vs delivery latency |
| SQL vs NoSQL for messages | NoSQL append log | Easier scale; harder ad-hoc queries |

**Related designs:** WhatsApp (similar), Facebook News Feed (different — fan-out feed vs point-to-point chat).

---

## Study Checklist

- [x] Step 1: Requirements
- [x] Step 2: Capacity
- [ ] Step 3: Write API contracts + WebSocket event shapes
- [ ] Step 4: Draw ER diagram; justify Cassandra vs MySQL
- [x] Step 5: High-level design + message workflow (ack pipeline)
- [x] Step 6: Pull vs push, long polling, connection registry, offline handling, 10K servers
- [ ] Step 7: Push, security, monitoring
- [ ] Step 8: Compare with WhatsApp / Slack

**References:** `SYSTEM_DESIGN_TEMPLATE.md`, [System Design Primer — Messenger](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/messenger/README.md)
