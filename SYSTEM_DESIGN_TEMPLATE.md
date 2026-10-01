# System Design Interview Template

## Overview
This template provides a structured approach to solving any system design problem. Follow this pattern step-by-step to ensure comprehensive coverage of all aspects.

---

## Step 1: Problem Understanding & Requirements Clarification

### 1.1 Problem Statement
- **What is the system?** (e.g., URL shortening service like TinyURL)
- **What does it do?** (e.g., creates short aliases for long URLs)
- **Similar services?** (e.g., bit.ly, goo.gl, qlink.me)
- **Difficulty Level:** Easy/Medium/Hard

### 1.2 Functional Requirements
List the core features the system must support:
1. [Feature 1]
2. [Feature 2]
3. [Feature 3]
4. [Feature 4]

### 1.3 Non-Functional Requirements
Define quality attributes:
1. **Availability:** How available should the system be? (e.g., 99.9%, 99.99%)
2. **Performance:** What latency requirements? (e.g., real-time, <100ms)
3. **Scalability:** Expected growth? (e.g., 100M users, 1B requests/day)
4. **Reliability:** How fault-tolerant?
5. **Security:** Any security concerns?
6. **Consistency:** Strong consistency or eventual consistency OK?

### 1.4 Extended Requirements (Optional)
Additional features that might be nice-to-have:
1. [Feature 1]
2. [Feature 2]
3. [Other features]

---

## Step 2: Capacity Estimation (BTSM Framework)

Use the **BTSM** mnemonic: **B**andwidth, **T**raffic, **S**torage, **M**emory (Cache)

### 2.1 Traffic Estimation
- **Read/Write Ratio:** Determine if system is read-heavy or write-heavy
- **Queries Per Second (QPS):**
  - Write QPS = [Total writes per month] / (30 days × 24 hours × 3600 seconds)
  - Read QPS = Write QPS × Read/Write Ratio

**Quick Calculation Tip:**
- **Exact:** 30 days × 24 hours × 3600 seconds = **2,592,000 seconds**
- **For quick mental math:** Use **2.5 million seconds** (easier to divide)
  - Example: 500M per month / 2.5M = 200/s
  - Close enough for interview calculations!

### 2.2 Storage Estimation
- **Total Objects:** [Objects per month] × [Retention period in months]
- **Size per Object:** Estimate bytes per object
  - Break down each field in your data model
  - Account for database overhead (row headers, indexes, padding)
  - Consider average vs maximum sizes
- **Total Storage:** Total Objects × Size per Object

### 2.3 Bandwidth Estimation
- **Incoming (Write):** Write QPS × Size per Object
- **Outgoing (Read):** Read QPS × Size per Object

### 2.4 Memory (Cache) Estimation
- **Cache Strategy:** What percentage of traffic should be cached?
- **Cache Size:** [Percentage] × [Daily requests] × [Size per object]
- **Note:** Actual usage may be less due to duplicate requests

### 2.5 Summary Table
| Metric | Value |
|--------|-------|
| Write QPS | [value] |
| Read QPS | [value] |
| Incoming Data | [value] |
| Outgoing Data | [value] |
| Storage (retention period) | [value] |
| Memory for Cache | [value] |

---

## Step 3: System APIs

Define the API contracts. Use REST APIs for simplicity and scalability.

### 3.1 Create Resource (POST)
**Endpoint:** `POST /api/v1/[resource]`

**Request Headers:**
- `Authorization: Bearer {token}` (if authentication required)
- `Content-Type: application/json`

**Request Body:**
```json
{
  "field1": "value1",
  "field2": "value2"
}
```

**Success Response (201 Created):**
```json
{
  "id": "resource_id",
  "field1": "value1",
  "created_at": "2025-01-15T10:30:00Z"  // ISO 8601 format
}
```

**Date/Time Format: ISO 8601**
- **ISO** = **International Organization for Standardization**
- **8601** = The standard number assigned by ISO (just a sequential number)
- **ISO 8601** = International standard #8601 for date and time representation
- Ensures consistent date/time formatting across systems and countries
- Format: `YYYY-MM-DDTHH:mm:ssZ` or `YYYY-MM-DDTHH:mm:ss+HH:mm`

**Why "8601"?**
- ISO assigns sequential numbers to standards
- ISO 8601 was published in 1988 (revised in 2000, 2004, 2019)
- The number "8601" is just the standard's identifier - it doesn't have special meaning
- Other ISO standards: ISO 9001 (quality management), ISO 27001 (information security), etc.
- Think of it like a catalog number or document ID

**ISO 8601 Examples:**
```
Date only:           2025-01-15
Date and time:       2025-01-15T10:30:00
With timezone (UTC): 2025-01-15T10:30:00Z
With timezone:       2025-01-15T10:30:00+05:30
With milliseconds:   2025-01-15T10:30:00.123Z
```

**Components:**
- **YYYY:** 4-digit year
- **MM:** 2-digit month (01-12)
- **DD:** 2-digit day (01-31)
- **T:** Separator between date and time
- **HH:** 2-digit hour (00-23, 24-hour format)
- **mm:** 2-digit minute (00-59)
- **ss:** 2-digit second (00-59)
- **Z:** UTC timezone indicator (Zulu time)
- **+HH:mm or -HH:mm:** Timezone offset from UTC

**Why Use ISO 8601?**
- ✅ **Unambiguous:** No confusion about date format (MM/DD vs DD/MM)
- ✅ **Sortable:** Lexicographically sortable (string sort = chronological sort)
- ✅ **International:** Works across all countries and languages
- ✅ **Standard:** Widely supported by APIs, databases, programming languages
- ✅ **Timezone-aware:** Can specify timezone explicitly

**Error Responses:**
- `400 Bad Request`: Invalid input, malformed request
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: Authenticated but insufficient permissions
- `404 Not Found`: Resource does not exist
- `409 Conflict`: Resource already exists (duplicate)
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### 3.2 Get Resource (GET)
**Endpoint:** `GET /api/v1/[resource]/{id}`

**Success Response (200 OK):**
```json
{
  "id": "resource_id",
  "field1": "value1"
}
```

**Error Responses:**
- `404 Not Found`: Resource does not exist
- `500 Internal Server Error`: Server error

### 3.3 Update Resource (PUT/PATCH)
**Endpoint:** `PUT /api/v1/[resource]/{id}`

**Success Response (200 OK):**
- PUT returns `200 OK` (not 201) because it updates an existing resource
- Include updated resource in response body

**Error Responses:**
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Not authorized to update this resource
- `404 Not Found`: Resource does not exist
- `409 Conflict`: Update conflicts with current state
- `500 Internal Server Error`: Server error

### 3.4 Delete Resource (DELETE)
**Endpoint:** `DELETE /api/v1/[resource]/{id}`

**Success Response:**
- **204 No Content** (preferred): No response body, resource deleted
- **200 OK** (alternative): With body if you want to return metadata

**Error Responses:**
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Not authorized to delete this resource
- `404 Not Found`: Resource does not exist
- `500 Internal Server Error`: Server error

### 3.5 Rate Limiting & Abuse Prevention

**Rate Limiting Strategy:**
- Define rate limits per user/tier (e.g., 100 requests/day for free tier)
- Track rate limits in Redis or similar fast storage
- Return `429 Too Many Requests` when limit exceeded (not 403)

**Rate Limit Headers:**
Add these headers to **every response** (success and error):
```
X-RateLimit-Limit: 100          // Total requests allowed in time window
X-RateLimit-Remaining: 45        // Requests remaining in current window
X-RateLimit-Reset: 1640995200   // Unix timestamp when limit resets
```

**Why "X-" Prefix?**

The **"X-" prefix** in HTTP headers indicates a **custom/non-standard header**.

**History:**
- **RFC 6648 (2012):** Deprecated the "X-" prefix convention
- **Before 2012:** "X-" was used to indicate experimental/custom headers
- **After 2012:** "X-" prefix is discouraged, but still widely used

**Why It's Still Used:**
- ✅ **Convention:** Widely adopted convention (GitHub, Twitter, etc. use it)
- ✅ **Clarity:** Makes it obvious these are custom headers, not standard HTTP headers
- ✅ **Avoids conflicts:** Prevents collision with future standard headers
- ✅ **Backward compatibility:** Many systems already use "X-" headers

**Examples of X- Headers:**
- `X-RateLimit-Limit` - Rate limiting (custom)
- `X-Request-ID` - Request tracking (custom)
- `X-Forwarded-For` - Proxy information (now standardized as `Forwarded`)
- `X-API-Key` - API authentication (custom)
- `X-Custom-Header` - Any custom header

**Standard vs Custom Headers:**
- **Standard headers:** `Content-Type`, `Authorization`, `User-Agent` (no prefix)
- **Custom headers:** `X-RateLimit-Limit`, `X-Request-ID` (X- prefix)

**Modern Approach:**
- **Best practice:** Use descriptive names without "X-" if possible
- **Examples:** `RateLimit-Limit`, `Request-ID` (without X-)
- **Reality:** "X-" is still very common and widely accepted

**For Rate Limiting:**
- Common convention: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- Used by: GitHub API, Twitter API, Stripe API, etc.
- Alternative: `RateLimit-Limit` (without X-, but less common)

**Implementation:**
- Check rate limit counter before processing request
- Decrement counter if under limit
- Add headers to response in middleware/filter
- Return `429` with headers if limit exceeded

**Additional Abuse Prevention:**
- IP-based rate limiting
- Input validation
- Monitoring for suspicious patterns

### 3.6 HTTP Status Codes Reference

**2xx Success Codes:**

| Code | Name | When to Use |
|------|------|-------------|
| **200** | OK | Standard success response for GET, PUT, PATCH requests |
| **201** | Created | Resource successfully created (POST requests) |
| **202** | Accepted | Request accepted but processing not complete (async operations) |
| **203** | Non-Authoritative Information | Success but metadata may have been modified |
| **204** | No Content | Success with no response body (DELETE, PUT without response) |
| **205** | Reset Content | Success, client should reset the view/form |
| **206** | Partial Content | Partial content returned (used with Range headers for file downloads) |

**3xx Redirection Codes:**

| Code | Name | When to Use |
|------|------|-------------|
| **300** | Multiple Choices | Multiple options available (rarely used) |
| **301** | Moved Permanently | Resource permanently moved to new URL (use for URL redirects) |
| **302** | Found | Temporary redirect (most common redirect) |
| **303** | See Other | Redirect to another resource (after POST) |
| **304** | Not Modified | Resource not modified (caching - no body returned) |
| **305** | Use Proxy | Must use proxy (deprecated, rarely used) |
| **307** | Temporary Redirect | Temporary redirect (preserves HTTP method) |
| **308** | Permanent Redirect | Permanent redirect (preserves HTTP method) |

**4xx Client Error Codes:**

| Code | Name | When to Use |
|------|------|-------------|
| **400** | Bad Request | Invalid request syntax, malformed JSON, missing required fields |
| **401** | Unauthorized | Missing or invalid authentication credentials |
| **402** | Payment Required | Reserved for future use (payment systems) |
| **403** | Forbidden | Authenticated but insufficient permissions |
| **404** | Not Found | Resource does not exist |
| **405** | Method Not Allowed | HTTP method not allowed for this endpoint |
| **406** | Not Acceptable | Server cannot produce response matching Accept header |
| **407** | Proxy Authentication Required | Authentication required for proxy |
| **408** | Request Timeout | Client did not send request within server's time limit |
| **409** | Conflict | Resource conflict (duplicate entry, version conflict) |
| **410** | Gone | Resource permanently removed (more specific than 404) |
| **411** | Length Required | Content-Length header required |
| **412** | Precondition Failed | Condition in request headers not met |
| **413** | Payload Too Large | Request body too large (file upload limits) |
| **414** | URI Too Long | URL too long |
| **415** | Unsupported Media Type | Media type not supported |
| **416** | Range Not Satisfiable | Range header cannot be satisfied |
| **417** | Expectation Failed | Expect header cannot be met |
| **418** | I'm a teapot | April Fools' joke (RFC 2324) - sometimes used for humorous errors |
| **421** | Misdirected Request | Request sent to wrong server |
| **422** | Unprocessable Entity | Valid syntax but semantic errors (validation failures) |
| **423** | Locked | Resource is locked |
| **424** | Failed Dependency | Request failed due to dependency failure |
| **425** | Too Early | Server unwilling to process request (HTTP/2) |
| **426** | Upgrade Required | Client should switch protocols |
| **428** | Precondition Required | Origin server requires conditional request |
| **429** | Too Many Requests | Rate limit exceeded (critical for API design!) |
| **431** | Request Header Fields Too Large | Headers too large |
| **451** | Unavailable For Legal Reasons | Censored for legal reasons |

**5xx Server Error Codes:**

| Code | Name | When to Use |
|------|------|-------------|
| **500** | Internal Server Error | Generic server error (catch-all) |
| **501** | Not Implemented | Server doesn't support the functionality |
| **502** | Bad Gateway | Invalid response from upstream server |
| **503** | Service Unavailable | Server temporarily unavailable (maintenance, overload) |
| **504** | Gateway Timeout | Upstream server didn't respond in time |
| **505** | HTTP Version Not Supported | HTTP version not supported |
| **506** | Variant Also Negotiates | Internal server configuration error |
| **507** | Insufficient Storage | Server cannot store representation |
| **508** | Loop Detected | Infinite loop detected |
| **510** | Not Extended | Further extensions required |
| **511** | Network Authentication Required | Network access authentication required |

**Common Status Codes for System Design Interviews:**

**Most Frequently Used:**
- **200 OK** - Success
- **201 Created** - Resource created
- **204 No Content** - Success with no body
- **301/302** - Redirects
- **304 Not Modified** - Caching
- **400 Bad Request** - Invalid input
- **401 Unauthorized** - Not authenticated
- **403 Forbidden** - Not authorized
- **404 Not Found** - Resource missing
- **409 Conflict** - Duplicate/resource conflict
- **413 Payload Too Large** - File size limits
- **429 Too Many Requests** - Rate limiting
- **500 Internal Server Error** - Server error
- **503 Service Unavailable** - Maintenance/overload

**Custom Status Codes (6xx and beyond):**

**How to Use Custom Codes:**
- **Range:** 6xx-9xx are not officially assigned
- **Best Practice:** Avoid custom codes if possible - use existing codes with custom error messages
- **When to Use:** Only if you need specific error types not covered by standard codes

**Example Custom Code Usage:**
```json
// Instead of custom 600, use 400 with custom error code in body
{
  "error": {
    "code": "CUSTOM_ERROR_600",
    "message": "Custom business logic error",
    "status": 400
  }
}
```

**If You Must Use Custom Codes:**
- Document them clearly in API documentation
- Use 6xx range (600-699) for application-specific errors
- Include error details in response body
- Ensure clients can handle unknown status codes gracefully

**Example:**
```
600 - Business Rule Violation
601 - Account Suspended
602 - Quota Exceeded
```

**Recommendation:** Use standard HTTP codes (200-599) with custom error codes in the response body for better compatibility and standards compliance.

---

## Step 4: Database Design

### 4.1 Data Models
Define the schema with all fields and their types:
- Primary keys
- Foreign keys
- Indexes needed
- Constraints

**NoSQL Schema Representation:**

**Is NoSQL Schema Always JSON?**

Not always! It depends on the NoSQL database type:

1. **Document Databases (MongoDB, DynamoDB):** ✅ Yes, typically JSON/JSON-like
2. **Key-Value Stores (Redis, Riak):** ⚠️ Usually JSON, but can be any format
3. **Column-Family (Cassandra, HBase):** ❌ No, uses column-family structure
4. **Graph Databases (Neo4j):** ❌ No, uses graph/node structure

**Document Database Schema (DynamoDB/MongoDB) - JSON Format:**
```json
{
  "id": "resource_id",
  "field1": "value1",
  "field2": "value2",
  "created_at": "2025-01-15T10:30:00Z"
}
```

**Column-Family Schema (Cassandra) - Different Format:**
```
Table: resources
Partition Key: id
Clustering Columns: created_at

Column Family Structure:
id (partition key) | created_at | field1 | field2
--------------------|------------|--------|--------
resource_1         | 2025-01-15 | value1 | value2
```

**Key-Value Store Schema (Redis/Riak) - Simple Format:**
```
Key: "resource:resource_id"
Value: {
  "field1": "value1",
  "field2": "value2",
  "created_at": "2025-01-15T10:30:00Z"
}
```

**Summary:**
- **Document/Key-Value databases:** Often use JSON representation ✅
- **Column-Family databases:** Use column-family structure, but JSON is common in docs ⚠️
- **Graph databases:** Use node/relationship structure ❌
- **In practice:** JSON is commonly used in documentation for clarity, even for non-JSON databases

**What is a Foreign Key?**
- A **foreign key** is a column (or set of columns) in one table that references the primary key of another table
- Creates a link/relationship between two tables
- Ensures data consistency across related tables

**Example:**
```sql
-- User table (parent/referenced table)
CREATE TABLE User (
    UserID INT PRIMARY KEY,  -- Primary key
    Name VARCHAR(20)
);

-- URL table (child/referencing table)
CREATE TABLE URL (
    Hash VARCHAR(16) PRIMARY KEY,
    UserID INT,  -- Foreign key column
    FOREIGN KEY (UserID) REFERENCES User(UserID)  -- Foreign key constraint
);
```

**What is Referential Integrity?**
- **Referential integrity** ensures that relationships between tables remain consistent
- Prevents "orphaned" records (records that reference non-existent data)
- Database enforces rules automatically

**Referential Integrity Rules:**
1. **Insert Rule:** Can't insert a record with foreign key value that doesn't exist in referenced table
2. **Update Rule:** Can't update primary key if other tables reference it (unless CASCADE)
3. **Delete Rule:** Can't delete a record if other tables reference it (unless CASCADE or SET NULL)

**Benefits of Foreign Keys:**
- ✅ **Data consistency:** Prevents invalid references
- ✅ **Data integrity:** Ensures relationships are valid
- ✅ **Automatic validation:** Database enforces rules
- ✅ **Documentation:** Makes relationships explicit in schema

**Trade-offs:**
- ⚠️ **Performance:** Slight overhead on inserts/updates (must check foreign key)
- ⚠️ **Flexibility:** Can make schema changes more complex
- ⚠️ **Cascading:** Need to handle CASCADE/SET NULL/SET DEFAULT carefully

**What is Cascading?**

**Cascading** defines what happens to child records when a parent record is updated or deleted. It's a foreign key constraint option that automatically propagates changes.

**Cascade Options:**

1. **CASCADE:** Automatically update/delete child records when parent is updated/deleted
2. **SET NULL:** Set foreign key to NULL when parent is deleted
3. **SET DEFAULT:** Set foreign key to default value when parent is deleted
4. **RESTRICT/NO ACTION:** Prevent parent deletion if children exist (default behavior)

**Example with CASCADE:**
```sql
CREATE TABLE User (
    UserID INT PRIMARY KEY,
    Name VARCHAR(20)
);

CREATE TABLE URL (
    Hash VARCHAR(16) PRIMARY KEY,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
        ON DELETE CASCADE      -- Delete URLs when User is deleted
        ON UPDATE CASCADE      -- Update UserID in URLs when User.UserID changes
);

-- Delete user
DELETE FROM User WHERE UserID = 123;
-- Result: User deleted AND all URLs with UserID=123 are automatically deleted
```

**Example with SET NULL:**
```sql
CREATE TABLE URL (
    Hash VARCHAR(16) PRIMARY KEY,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
        ON DELETE SET NULL    -- Set UserID to NULL when User is deleted
);

-- Delete user
DELETE FROM User WHERE UserID = 123;
-- Result: User deleted, URLs with UserID=123 have UserID set to NULL
```

**Example with RESTRICT:**
```sql
CREATE TABLE URL (
    Hash VARCHAR(16) PRIMARY KEY,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
        ON DELETE RESTRICT    -- Prevent deletion if URLs exist
);

-- Try to delete user
DELETE FROM User WHERE UserID = 123;
-- Result: ERROR - Cannot delete User because URLs reference it
```

**When to Use Each:**
- **CASCADE:** Child records have no meaning without parent (e.g., delete user → delete URLs)
- **SET NULL:** Child records can exist independently (e.g., URLs can be anonymous)
- **SET DEFAULT:** Child records should have default parent
- **RESTRICT:** Child records must always have valid parent (safest, default)

### 4.2 Database Choice
- **SQL vs NoSQL:** Choose based on requirements
  - SQL: Strong consistency, ACID transactions, complex queries
  - NoSQL: High scalability, flexible schema, eventual consistency
- **Specific Database:** MySQL, PostgreSQL, MongoDB, Cassandra, etc.

### 4.3 Sharding Strategy
- **Sharding Key:** What field to use for partitioning?
- **Number of Shards:** How many shards needed?
- **Replication:** Master-slave, multi-master, etc.

### 4.4 Indexing

**What is a Database Index?**

An **index** is a data structure that improves the speed of data retrieval operations on a database table. Think of it like an index in a book - instead of reading every page to find a topic, you look it up in the index.

**How Indexes Work:**
- Creates a separate data structure (usually B-tree or hash table)
- Stores sorted copies of indexed column values + pointers to actual rows
- Allows fast lookups without scanning entire table

**What is a B-Tree?**

A **B-tree** (Balanced Tree) is a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time.

**B-Tree Properties:**
- **Balanced:** All leaf nodes are at the same depth
- **Sorted:** Data is stored in sorted order (left to right)
- **Multi-way:** Each node can have multiple children (not just 2 like binary tree)
- **Order (m):** Maximum number of children (typically 100-1000, depends on page size)

**How B-Tree Makes Lookups Faster:**

**1. Logarithmic Time Complexity:**
- **Without index:** O(n) - must check every row
- **With B-tree:** O(log n) - only traverse tree height
- **Example:** 1 billion rows → ~30 comparisons instead of 1 billion

**2. Reduced Disk I/O:**
- B-tree nodes fit in disk pages (4KB-16KB)
- Each node access = 1 disk read
- Example: 1 billion rows → ~30 disk reads instead of 1 billion

**3. Sequential Access:**
- Leaf nodes are linked (can traverse in order)
- Efficient for range queries (WHERE column BETWEEN X AND Y)

**How B-Tree Makes Joins Faster:**

**Without Indexes:**
- Scan both tables: O(n × m) - very slow!

**With B-Tree Indexes:**
- Lookup in first table: O(log n)
- Lookup in second table: O(log m)
- Total: O(log n + log m) - much faster!

**Join Strategy:**
```
For each row in first table:
  1. Use B-tree index on second table to find matching rows
  2. O(log n) lookup per row
  3. Much faster than scanning entire second table
```

**Why B-Tree for Databases:**
- ✅ **Disk-Optimized:** Nodes sized to fit disk pages, minimizes I/O
- ✅ **Balanced:** Always maintains balance, guarantees O(log n)
- ✅ **Range Queries:** Leaf nodes linked sequentially, efficient for BETWEEN
- ✅ **Handles Large Data:** Works well with billions of rows

**Why Use Indexes?**

✅ **Faster Reads:**
- **Without index:** Full table scan (check every row) - O(n) time
- **With index:** Index lookup (binary search) - O(log n) time
- **Speedup:** Can be 100x-1000x faster for large tables

✅ **Faster Joins:** Foreign key lookups are much faster with indexes
✅ **Faster Sorting:** ORDER BY queries are faster if column is indexed
✅ **Faster Filtering:** WHERE clauses on indexed columns are much faster

**Performance Impact:**

**Reads (SELECT queries):**
- ✅ **Much faster** with index
- Example: Finding records by indexed column
  - Without index: Scan all rows = seconds/minutes
  - With index: Lookup in index = milliseconds

**Writes (INSERT/UPDATE/DELETE):**
- ⚠️ **Slightly slower** with index
- Must update both table AND index
- Example: Inserting new record
  - Without index: Insert 1 row
  - With index: Insert 1 row + update index = ~10-20% slower

**Space Usage:**

**Index Storage:**
- Indexes take additional disk space
- Typically 10-30% of table size (depends on column type and data)
- Example: 1TB table might need 100-300GB for indexes

**Index Size Calculation:**
```
Index on column (INT):
- Column value: 4 bytes (INT)
- Row pointer: 4-8 bytes (depends on database)
- Overhead: ~10-20% (B-tree structure)
- Per index entry: ~10-15 bytes

For 1 billion rows:
- Index size: 1B × 12 bytes = 12GB
- Plus overhead: ~14-15GB total
```

**When to Use Indexes:**

✅ **Use indexes on:**
- Primary keys (automatic)
- Foreign keys (for join performance)
- Columns used in WHERE clauses frequently
- Columns used in ORDER BY
- Columns used in JOIN conditions

❌ **Don't use indexes on:**
- Columns rarely queried
- Columns with very few unique values (low cardinality)
- Columns frequently updated (high write overhead)
- Small tables (index overhead not worth it)

**Index Types:**

1. **Primary Index (Primary Key):** Automatically created, unique, fastest lookups
2. **Secondary Index:** Created on non-primary key columns, can be unique or non-unique
3. **Composite Index:** Index on multiple columns, useful for multi-column queries

**Index Trade-offs:**

| Aspect | Without Index | With Index |
|--------|---------------|------------|
| **Read Speed** | Slow (full scan) | Fast (index lookup) |
| **Write Speed** | Fast | Slightly slower (must update index) |
| **Space** | Table only | Table + Index (10-30% more) |
| **Maintenance** | None | Index must be maintained |

**Consider trade-off:** Faster reads vs slower writes

---

## Step 5: High-Level Design

### 5.1 System Architecture Diagram
```
[Client] → [Load Balancer] → [Application Servers] → [Database]
                              ↓
                         [Cache Layer]
                              ↓
                         [CDN (if needed)]
```

### 5.2 Core Components
1. **Load Balancer:** Distributes incoming requests
2. **Application Servers:** Handle business logic
3. **Database:** Stores data
4. **Cache:** Stores frequently accessed data
5. **CDN:** (If needed) For static content
6. **Message Queue:** (If needed) For async processing

---

## Step 6: Detailed Design

### 6.1 Core Algorithms
- How does the main functionality work?
- What algorithms are used?
- How are collisions/conflicts handled?

### 6.2 Caching Strategy
- **What to Cache:** Hot data (80-20 rule)
- **Cache Eviction:** LRU, LFU, TTL, etc.
- **Cache Location:** Application servers, Redis, CDN

### 6.3 Load Balancing
- **Strategy:** Round-robin, Least connections, Consistent hashing
- **Health Checks:** Monitor server health

### 6.4 Database Sharding
- **Sharding Key:** How to partition data
- **Replication:** Read replicas for scaling reads
- **Consistency:** Strong vs eventual consistency

---

## Step 7: Additional Considerations

### 7.1 Security
- Authentication & Authorization
- Rate limiting to prevent abuse
- Input validation
- Encryption (at rest, in transit)

### 7.2 Analytics & Monitoring
- What metrics to track?
- Where to store analytics data?
- Monitoring & alerting setup

### 7.3 Scaling Strategies
- **Horizontal Scaling:** Add more servers
- **Vertical Scaling:** Increase server capacity
- **Database Scaling:** Read replicas, sharding
- **Cache Scaling:** Distributed cache cluster

### 7.4 Failure Handling
- What happens when components fail?
- Redundancy strategies
- Disaster recovery

---

## Step 8: Trade-offs & Alternatives

### 8.1 Design Trade-offs
- **Consistency vs Availability:** Choose based on CAP theorem
- **Latency vs Cost:** More cache = lower latency but higher cost
- **Complexity vs Performance:** Simpler design vs optimized performance

### 8.2 Alternative Approaches
- **Alternative 1:** [Description]
  - Pros: [List]
  - Cons: [List]
- **Alternative 2:** [Description]
  - Pros: [List]
  - Cons: [List]

---

## Key Concepts Reference

### Sharding
**What is Sharding?**
- Sharding is a database partitioning technique where data is split across multiple databases/servers (shards)
- Each shard contains a subset of the total data
- Helps scale horizontally when a single database becomes too large

**Write Sharding:**
- Distributing write operations across multiple shards
- Each write goes to a specific shard based on a sharding key (e.g., hash of user_id)
- Reduces write load on any single database

**Read Sharding:**
- Distributing read operations across shards
- Can read from specific shard or aggregate from multiple shards
- Often combined with read replicas for better performance

### CDN (Content Delivery Network)
**What is CDN?**
- A network of geographically distributed servers that cache content closer to users
- Reduces latency by serving content from nearest edge server
- Reduces load on origin servers

**How it works:**
1. User requests content
2. Request routed to nearest CDN edge server
3. If cached, served immediately
4. If not cached, fetched from origin, cached, then served

**Use cases:**
- Static content (images, videos, CSS, JS)
- API responses (if cacheable)
- Global distribution

### Distributed SQL vs NoSQL

**Distributed SQL:**
- Examples: Google Spanner, CockroachDB, Amazon Aurora
- ACID transactions across distributed nodes
- Strong consistency guarantees
- SQL query language
- Good for: Financial systems, inventory management (need strong consistency)

**NoSQL:**
- Examples: MongoDB, Cassandra, DynamoDB, Redis
- Flexible schema
- Horizontal scaling easier
- Eventual consistency (usually)
- Good for: High-volume reads, flexible data models, rapid development

**Key Differences:**

| Aspect | Distributed SQL | NoSQL |
|--------|----------------|-------|
| Consistency | Strong | Eventual (usually) |
| Transactions | ACID across nodes | Limited/None |
| Schema | Fixed | Flexible |
| Scaling | Complex | Easier horizontal |
| Query Language | SQL | Various (document, key-value, etc.) |
| Use Case | Critical data, transactions | High volume, flexible needs |

### Database Compression

**What is DB Compression?**
- Technique to reduce storage space by encoding data more efficiently
- Reduces I/O operations (less data to read/write)
- Trade-off: CPU overhead for compression/decompression

**How it happens:**
1. **Row-level compression:**
   - Eliminate redundant data within a row
   - Use shorter representations for common values
   - Example: NULL values stored efficiently

2. **Page-level compression:**
   - Compress entire database pages
   - Common patterns identified and compressed
   - Example: SQL Server page compression

3. **Column-level compression:**
   - Compress data column by column
   - Effective when columns have repeated values
   - Example: Parquet format

4. **Dictionary compression:**
   - Create dictionary of unique values
   - Store references instead of full values
   - Example: "United States" → 1, "USA" → 1

**Benefits:**
- Reduced storage costs
- Faster backups/restores
- Less network transfer
- More data fits in cache

**Trade-offs:**
- CPU overhead
- Slightly slower writes
- Faster reads (less I/O)

### Edge Caching

**What is Edge Caching?**
- Caching content at edge locations (closer to end users)
- Part of CDN functionality
- Reduces latency and origin server load

**How it works:**
1. Content cached at edge servers (geographically distributed)
2. User request goes to nearest edge server
3. If cache hit → served immediately
4. If cache miss → fetch from origin, cache, then serve

**Edge Caching vs Application Caching:**
- **Edge Caching:** At network edge (CDN), closer to users geographically
- **Application Caching:** In application servers (Redis, Memcached), closer to application logic

**Use cases:**
- Static assets (images, videos)
- API responses (if cacheable)
- HTML pages (if static or semi-static)

### Read Bandwidth Optimization

**How to optimize Read bandwidth:**

1. **Caching:**
   - Cache frequently accessed data
   - Reduces database reads
   - Example: Cache hot data in Redis

2. **CDN:**
   - Serve static content from CDN
   - Reduces origin server bandwidth
   - Example: Serve images, videos from CDN

3. **Read Replicas:**
   - Distribute read traffic across replicas
   - Reduces load on primary database
   - Example: 1 write master, 5 read replicas

4. **Data Compression:**
   - Compress responses (gzip, brotli)
   - Reduces network transfer
   - Example: Compress JSON responses

5. **Pagination:**
   - Return data in chunks
   - Reduces response size
   - Example: Return 20 items per page instead of 1000

6. **Field Selection:**
   - Return only needed fields
   - Reduces payload size
   - Example: GraphQL field selection

7. **Edge Caching:**
   - Cache at edge locations
   - Reduces origin bandwidth
   - Example: Cache API responses at CDN edge

8. **Connection Pooling:**
   - Reuse database connections
   - Reduces connection overhead
   - Example: Connection pool of 100 connections

### UUID (Universally Unique Identifier)

**What is UUID?**
- A 128-bit identifier that is unique across time and space
- Standard format: 8-4-4-4-12 hexadecimal digits
- **Total characters:** 36 characters (32 hex digits + 4 hyphens)
- **Example:** `550e8400-e29b-41d4-a716-446655440000`

**What does "Unique Across Time and Space" mean?**

This means a UUID is designed to be unique:
- **Across Time:** Even if generated at different times (yesterday, today, tomorrow), each UUID will be different
- **Across Space:** Even if generated on different machines, networks, or locations, each UUID will be different

**Why this matters:**
- **No central authority needed:** You don't need a central server to assign unique IDs
- **Distributed systems:** Multiple servers can generate UUIDs independently without collisions
- **Global uniqueness:** UUIDs generated anywhere in the world at any time should be unique

**Example:**
- Server A in New York generates UUID: `abc123...`
- Server B in London generates UUID: `def456...` (different, even without coordination)
- Server A generates another UUID tomorrow: `ghi789...` (different from yesterday's)

**Note:** "Unique" means "practically unique" - the probability of collision is extremely low (about 1 in 2^122 for UUID4), but not mathematically impossible.

**Storage Size:**
- **As string (VARCHAR):** 36 bytes (36 characters × 1 byte each)
- **As binary (BINARY(16)):** 16 bytes (128 bits = 16 bytes)
- **Recommendation:** Store as BINARY(16) to save space, convert to string when needed

**How 36 Hex Characters = 16 Bytes?**

The hyphens in UUID format are just for readability - they're not part of the actual data!

**Step-by-step conversion:**
1. **UUID string:** `550e8400-e29b-41d4-a716-446655440000`
2. **Remove hyphens:** `550e8400e29b41d4a716446655440000` (32 hex digits)
3. **Each hex digit = 4 bits:**
   - `0` = `0000` (binary)
   - `1` = `0001`
   - `5` = `0101`
   - `a` = `1010` (10 in decimal)
   - `f` = `1111` (15 in decimal)
4. **Two hex digits = 1 byte (8 bits):**
   - `55` = `01010101` = 85 (decimal) = 1 byte
   - `0e` = `00001110` = 14 (decimal) = 1 byte
   - `84` = `10000100` = 132 (decimal) = 1 byte
   - ... and so on
5. **32 hex digits ÷ 2 = 16 bytes**

**Example conversion:**
```
UUID: 550e8400-e29b-41d4-a716-446655440000
      └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘ └─────┬─────┘
       8      4      4      4        12 hex digits

Remove hyphens: 550e8400e29b41d4a716446655440000

Convert to bytes (each pair = 1 byte):
55 0e 84 00 e2 9b 41 d4 a7 16 44 66 55 44 00 00
│  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │
85 14 132 0  226 155 65 212 167 22 68 102 85 68 0 0 (decimal)

Total: 16 bytes (128 bits)
```

**Why this works:**
- Hexadecimal is base-16 (0-9, a-f = 16 values)
- Each hex digit represents 4 bits (2⁴ = 16)
- Two hex digits = 8 bits = 1 byte
- 32 hex digits = 16 bytes = 128 bits

**UUID4 (Random UUID):**
- **Generation:** Random/pseudo-random numbers
- **Uniqueness:** Based on randomness (very high probability of uniqueness)
- **Use cases:**
  - Primary keys in distributed systems
  - When you need non-sequential, non-guessable IDs
  - When you don't need deterministic generation
- **Example:** `f47ac10b-58cc-4372-a567-0e02b2c3d479`

**UUID5 (Name-based UUID using SHA-1):**
- **Generation:** Based on namespace + name, hashed with SHA-1
- **Uniqueness:** Deterministic - same namespace + name = same UUID
- **Use cases:**
  - When you need to generate the same UUID from the same input
  - Content-addressable storage
  - When you want reproducible IDs
- **Example:** UUID5 for namespace "URL" + name "https://example.com" always produces the same UUID

**How UUID5 Works (Detailed):**

**Step 1: Namespace UUID**

**What is a Namespace?**
- A **namespace** is a container or context that groups related identifiers together
- It prevents naming conflicts by creating separate "spaces" for different types of names
- Think of it like folders on your computer - same filename can exist in different folders

**Examples of Namespaces:**
- **DNS namespace:** For domain names (e.g., "example.com")
- **URL namespace:** For URLs (e.g., "https://example.com/page")
- **OID namespace:** For Object Identifiers (used in LDAP, X.500)
- **X.500 DN namespace:** For Distinguished Names (used in directory services)

**Why use namespaces in UUID5?**
- Same name in different namespaces = different UUID
- Example: "example.com" in DNS namespace ≠ "example.com" in URL namespace
- This prevents collisions when the same string might mean different things

**Common Namespace UUIDs (predefined standards):**
- **DNS namespace:** `6ba7b810-9dad-11d1-80b4-00c04fd430c8`
  - Use when generating UUIDs from domain names
- **URL namespace:** `6ba7b811-9dad-11d1-80b4-00c04fd430c8`
  - Use when generating UUIDs from URLs
- **OID namespace:** `6ba7b812-9dad-11d1-80b4-00c04fd430c8`
  - Use for Object Identifiers (OID)
- **X.500 DN namespace:** `6ba7b814-9dad-11d1-80b4-00c04fd430c8`
  - Use for Distinguished Names (DN)

**What are Object Identifiers (OID)?**

**OID** = **Object Identifier**

**Definition:**
- A globally unique identifier for objects, concepts, or entities
- Hierarchical numeric string (like a tree structure)
- Used in various standards: LDAP, SNMP, X.500, ASN.1, etc.

**Format:**
- Series of numbers separated by dots (e.g., `1.3.6.1.4.1.12345`)
- Each number represents a node in the hierarchy
- Left to right: Most general → Most specific

**OID Structure:**
```
1.3.6.1.4.1.12345
│ │ │ │ │ │ └─┬─┘
│ │ │ │ │ │   └─ Enterprise-specific ID
│ │ │ │ │ └───── Private enterprise (1)
│ │ │ │ └─────── Private (4)
│ │ │ └───────── Internet (1)
│ │ └─────────── DoD (6)
│ └───────────── ISO identified organization (3)
└─────────────── ISO (1)
```

**Common OID Examples:**
- `1.3.6.1.2.1` - Internet MIB (Management Information Base) for SNMP
- `1.3.6.1.4.1` - Private enterprise OIDs
- `2.5.4.3` - Common Name (CN) attribute in LDAP
- `2.5.4.6` - Country Name (C) attribute in LDAP

**Use Cases:**
- **LDAP (Lightweight Directory Access Protocol):** Identify attributes, object classes
- **SNMP (Simple Network Management Protocol):** Identify managed objects
- **X.500 Directory Services:** Identify directory objects
- **ASN.1 (Abstract Syntax Notation One):** Identify data types
- **PKI (Public Key Infrastructure):** Identify certificate attributes

**What are Distinguished Names (DN)?**

**DN** = **Distinguished Name**

**Definition:**
- A unique identifier for an entry in a directory service (like LDAP or X.500)
- Hierarchical path that uniquely identifies an object
- Like a file path, but for directory entries

**Format:**
- Series of attribute-value pairs separated by commas
- Each pair is an **RDN** (Relative Distinguished Name)
- Left to right: Most specific → Most general (opposite of file paths)

**DN Structure:**
```
CN=John Doe,OU=Engineering,O=Acme Corp,C=US
│  └─┬─┘  │  └────┬─────┘ │  └───┬───┘ │ └─┬─┘
│    │    │       │       │      │     │   └─ Country
│    │    │       │       │      │     └───── Organization
│    │    │       │       │      └─────────── Organizational Unit
│    │    │       │       └────────────────── Common Name
│    │    │       └────────────────────────── Attribute
│    │    └────────────────────────────────── Value
```

**Common DN Attributes:**
- **CN** (Common Name): Person's name or object name
- **OU** (Organizational Unit): Department or division
- **O** (Organization): Company name
- **C** (Country): Country code (e.g., US, UK)
- **L** (Locality): City or location
- **ST** (State/Province): State or province
- **DC** (Domain Component): Domain name component
- **UID** (User ID): User identifier

**DN Examples:**
```
# Person in a company
CN=John Doe,OU=Engineering,O=Acme Corp,C=US

# User in Active Directory
CN=John Doe,CN=Users,DC=acme,DC=com

# Server in organization
CN=mailserver,OU=IT,DC=acme,DC=com
```

**Use Cases:**
- **Active Directory:** Identify users, groups, computers
- **LDAP directories:** User authentication, address books
- **Email systems:** Identify email recipients
- **Certificate authorities:** Identify certificate subjects
- **Enterprise directories:** Employee directories, organizational charts

**DN vs OID:**
| Aspect | Distinguished Name (DN) | Object Identifier (OID) |
|--------|------------------------|------------------------|
| **Format** | Attribute=Value pairs (CN=John,OU=Sales) | Numeric dots (1.3.6.1.4.1) |
| **Readability** | Human-readable | Machine-readable |
| **Purpose** | Identify directory entries | Identify object types/attributes |
| **Example** | CN=John,OU=Sales,O=Acme | 2.5.4.3 (CN attribute) |
| **Usage** | LDAP, Active Directory | SNMP, LDAP schemas, ASN.1 |

**What is DNS?**
- **DNS** = **Domain Name System**
- Converts human-readable domain names (like "google.com") to IP addresses (like "142.250.191.14")
- Acts like a phone book for the internet
- Example: When you type "google.com", DNS looks up the IP address and routes you there

**Step 2: Concatenate Namespace + Name**
- Take the namespace UUID (16 bytes in binary)
- Append the name string (as bytes, UTF-8 encoded)
- This creates a combined byte array

**Step 3: SHA-1 Hash**

**What is SHA-1?**
- **SHA** = **Secure Hash Algorithm**
- **SHA-1** = Secure Hash Algorithm version 1
- A cryptographic hash function that takes input of any size and produces a fixed-size output (160 bits = 20 bytes)

**How SHA-1 Works:**
1. Takes input (can be any size - bytes, text, file, etc.)
2. Processes it through a mathematical algorithm
3. Produces a 160-bit (20-byte) hash value
4. Same input → always same hash
5. Small change in input → completely different hash

**SHA-1 Properties:**
- **Deterministic:** Same input always produces same output
- **One-way:** Can't reverse the hash to get original input
- **Avalanche effect:** Small input change causes large output change
- **Fixed size:** Always produces 20 bytes (160 bits)

**SHA-1 Usage:**
- **Data integrity:** Verify files haven't been corrupted
- **Digital signatures:** Sign documents/software
- **UUID5 generation:** Create deterministic UUIDs
- **Git:** Used to identify commits (though Git is moving to SHA-256)
- **Checksums:** Verify data transmission

**SHA-1 Example:**
```python
import hashlib

# SHA-1 hash
data = b"Hello World"
hash_obj = hashlib.sha1(data)
hash_hex = hash_obj.hexdigest()
# Result: "0a4d55a8d778e5022fab701977c5d840bbc486d0" (40 hex chars = 20 bytes)

# Same input = same hash
hash_obj2 = hashlib.sha1(b"Hello World")
hash_hex2 = hash_obj2.hexdigest()
# Result: Same "0a4d55a8d778e5022fab701977c5d840bbc486d0"

# Different input = different hash
hash_obj3 = hashlib.sha1(b"Hello World!")
hash_hex3 = hash_obj3.hexdigest()
# Result: Different hash
```

**Other SHA Variants:**

| SHA Version | Output Size | Security Level | Status |
|-------------|-------------|----------------|--------|
| **SHA-1** | 160 bits (20 bytes) | ⚠️ Deprecated (vulnerable) | Still used in UUID5, Git |
| **SHA-256** | 256 bits (32 bytes) | ✅ Secure | Recommended, widely used |
| **SHA-384** | 384 bits (48 bytes) | ✅ Secure | High security |
| **SHA-512** | 512 bits (64 bytes) | ✅ Secure | Highest security |
| **SHA-224** | 224 bits (28 bytes) | ✅ Secure | Less common |
| **SHA-512/224** | 224 bits (28 bytes) | ✅ Secure | Variant of SHA-512 |
| **SHA-512/256** | 256 bits (32 bytes) | ✅ Secure | Variant of SHA-512 |

**Why SHA-1 is Still Used in UUID5:**
- UUID5 standard was defined when SHA-1 was considered secure
- Changing it would break compatibility
- For UUID generation (not security), SHA-1 is still acceptable
- Modern systems use SHA-256 for new applications

**SHA-256 Example:**
```python
import hashlib

# SHA-256 (more secure, recommended)
data = b"Hello World"
hash_obj = hashlib.sha256(data)
hash_hex = hash_obj.hexdigest()
# Result: "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"
# 64 hex characters = 32 bytes = 256 bits
```

**Hash the combined byte array using SHA-1:**
- Input: namespace_bytes + name_bytes (combined byte array)
- Process: SHA-1 algorithm
- Output: 160-bit (20-byte) hash
- We use: First 16 bytes (for UUID, which is 128 bits)

**Step 4: Generate UUID from Hash**

**What are Version Bits?**
- UUIDs have a **version field** that indicates how the UUID was generated
- Stored in specific bit positions in the UUID
- Helps identify the UUID type and generation method

**UUID Version Bits Location:**
- Version bits are in the **time_hi_and_version** field
- **Byte position:** 7th byte (1-indexed) or byte 6 (0-indexed)
- **Bit position within UUID:** Bits 48-51 (counting from start of UUID, bit 0)
- **Bit position within byte 7:** Bits 0-3 (the 4 most significant bits of that byte)
- **Bit position within time_hi_and_version field:** Bits 12-15 (of the 16-bit field)
- Format: `xxxxxxxx-xxxx-Vxxx-xxxx-xxxxxxxxxxxx`
- The `V` position shows the version

**Note:** The version is in the **7th byte** (1-indexed). The bits are:
- **Bits 48-51** of the entire UUID (bits 0-3 of byte 7)
- These correspond to **bits 12-15** when counting within the time_hi_and_version field

**UUID Byte Structure:**
```
UUID: xxxxxxxx-xxxx-Vxxx-xxxx-xxxxxxxxxxxx
      └───┬───┘ └─┬─┘ └─┬─┘ └─┬─┘ └─────┬─────┘
         Bytes    Bytes  Bytes  Bytes    Bytes
         1-4      5-6    7-8    9-10     11-16
                  │      │
                  │      └─ Version bits here (byte 7, bits 12-15)
                  └──────── time_mid
```

**Detailed Breakdown:**
- **Bytes 1-4 (0-3 in 0-indexed):** time_low (8 hex digits) = bits 0-31
- **Bytes 5-6 (4-5 in 0-indexed):** time_mid (4 hex digits) = bits 32-47
- **Bytes 7-8 (6-7 in 0-indexed):** time_hi_and_version (4 hex digits) = bits 48-63
  - **Byte 7 (byte 6 in 0-indexed):** Contains version bits
  - **Version bits:** Bits 48-51 of UUID = bits 0-3 of byte 7 = bits 12-15 of time_hi_and_version field
  - These are the 4 most significant bits of byte 7
- **Bytes 9-10 (8-9 in 0-indexed):** clock_seq_hi_and_reserved + clock_seq_low = bits 64-79
- **Bytes 11-16 (10-15 in 0-indexed):** node (12 hex digits) = bits 80-127

**Version Bits in Binary:**
```
Byte 7 (time_hi_and_version, first byte of the 3rd group):
Within byte 7:  b7  b6  b5  b4  b3  b2  b1  b0
                └───┬───┘
                Version bits (bits 0-3 of byte 7)

Within UUID:    Bit 51 50 49 48 (bits 48-51 of entire UUID)
                └───┬───┘
                Version bits

For UUID5: version = 5 = 0101 in binary
So bits 48-51 of UUID = 0101
```

**UUID Versions:**
- **Version 1:** Time-based UUID (MAC address + timestamp)
- **Version 2:** DCE Security UUID (similar to v1, with POSIX UID/GID)
- **Version 3:** Name-based UUID using MD5 (deprecated)
- **Version 4:** Random UUID (most common)
- **Version 5:** Name-based UUID using SHA-1 (what we're using)

**What is MD5?**
- **MD5** = **Message Digest Algorithm 5**
- A cryptographic hash function (older than SHA-1)
- Produces a 128-bit (16-byte) hash value
- **Status:** ⚠️ **Deprecated and insecure** (vulnerable to collision attacks)
- **Why deprecated:** Security vulnerabilities discovered in 2004-2005
- **Still used in:** UUID3 (for backward compatibility), checksums (non-security use)

**MD5 vs SHA-1 vs SHA-256:**

| Hash Function | Output Size | Security | Status | Use Cases |
|---------------|-------------|----------|--------|-----------|
| **MD5** | 128 bits (16 bytes) | ❌ Broken | Deprecated | UUID3, non-security checksums |
| **SHA-1** | 160 bits (20 bytes) | ⚠️ Vulnerable | Deprecated | UUID5, Git (being phased out) |
| **SHA-256** | 256 bits (32 bytes) | ✅ Secure | Recommended | Modern applications, certificates |

**Why UUID3 Uses MD5:**
- UUID3 was defined in 1990s when MD5 was considered secure
- Changing it would break compatibility
- UUID3 is rarely used today (UUID5 with SHA-1 is preferred)
- For UUID generation (not security), MD5 is acceptable but not recommended for new code

**How Version Bits Work:**
```
Original hash bytes: [a1, b2, c3, d4, e5, f6, g7, h8, ...]
                      │   │   │   │   │   │   │   │
                      └───┴───┴───┴───┴───┴───┴───┘
                      Bytes 0-6 (0-indexed)

7th byte (byte 6 in 0-indexed) in binary: f6 = 1111 0110
                                          └─┬─┘
                                        version bits (bits 0-3 of byte 7)
                                        = bits 48-51 of entire UUID
                                        (4 most significant bits)

For UUID5: version = 5 = 0101 in binary
Replace upper 4 bits: 1111 0110 → 0101 0110 = 0x56

Result: Version bits now indicate this is a UUID5
```

**Bit Numbering Clarification:**
- **Within byte 7:** Version bits are bits 0-3 (the 4 most significant bits)
- **Within entire UUID:** Version bits are bits 48-51 (counting from bit 0 at start of UUID)
- **Within time_hi_and_version field:** Version bits are bits 12-15 (of the 16-bit field)
- All three refer to the same 4 bits, just different numbering systems

**Variant Bits:**
- Variant bits indicate the UUID layout/variant
- Stored in bits 6-7 of the 8th byte
- Standard variant: `10` (binary) = most significant bits are `10`
- Ensures UUID follows RFC 4122 standard

**Complete Process:**
1. Take first 16 bytes of SHA-1 hash (160 bits → use first 128 bits)
2. Set version bits: Replace bits 48-51 (upper 4 bits of byte 7) with `0101` (version 5)
3. Set variant bits: Replace bits 6-7 of 8th byte (byte 7, 0-indexed) with `10` (standard variant)
4. Result: A deterministic UUID that identifies as UUID5

**UUID5 Generation Summary:**
1. **Namespace UUID:** 32 hex digits = 16 bytes
2. **Name string:** Convert to bytes using UTF-8 encoding
3. **Combine:** namespace_bytes + name_bytes = combined byte array
4. **SHA-1 hash:** Hash the combined array → 20 bytes (160 bits)
5. **Take first 16 bytes:** Use first 128 bits for UUID
6. **Set version bits:** Mark as version 5
7. **Set variant bits:** Mark as standard variant
8. **Result:** UUID5 (deterministic, same input = same UUID)

**Example UUID5 Generation:**

```python
# Pseudo-code example
import hashlib

# Step 1: Define namespace (URL namespace)
namespace_uuid = "6ba7b811-9dad-11d1-80b4-00c04fd430c8"
name = "https://example.com"

# Step 2: Convert namespace UUID to binary (16 bytes)
namespace_bytes = uuid_to_bytes(namespace_uuid)
# Result: [107, 167, 184, 17, 157, 173, 17, 209, 128, 180, 0, 192, 79, 212, 48, 200]

# Step 3: Convert name to bytes (UTF-8)
name_bytes = name.encode('utf-8')
# Result: [104, 116, 116, 112, 115, 58, 47, 47, 101, 120, 97, 109, 112, 108, 101, 46, 99, 111, 109]

# Step 4: Concatenate
combined = namespace_bytes + name_bytes

# Step 5: SHA-1 hash
hash_bytes = hashlib.sha1(combined).digest()
# SHA-1 produces 20 bytes, we use first 16

# Step 6: Generate UUID from hash
uuid5 = hash_to_uuid(hash_bytes, version=5)
# Result: Always the same UUID for same namespace + name!
```

**Real Example:**
```python
# Python example
import uuid

# URL namespace (standard UUID)
URL_NAMESPACE = uuid.UUID('6ba7b811-9dad-11d1-80b4-00c04fd430c8')

# Generate UUID5
uuid1 = uuid.uuid5(URL_NAMESPACE, "https://example.com")
# Result: 5df41881-3aed-3515-88a7-2f4a814cf09e

uuid2 = uuid.uuid5(URL_NAMESPACE, "https://example.com")
# Result: 5df41881-3aed-3515-88a7-2f4a814cf09e (SAME!)

uuid3 = uuid.uuid5(URL_NAMESPACE, "https://google.com")
# Result: Different UUID (different name)
```

**Why Same Input = Same UUID:**
1. **Deterministic hashing:** SHA-1 always produces the same hash for the same input
2. **Fixed namespace:** Using the same namespace UUID ensures consistency
3. **Same name:** Same string input = same bytes = same hash = same UUID
4. **No randomness:** Unlike UUID4, UUID5 has no random component

**Use Case Example:**
- **Content-addressable storage:** Store file by content hash
  - Same file content → same UUID → can check if file already exists
- **Deduplication:** Generate UUID from content, detect duplicates
- **Reproducible IDs:** Need the same ID for the same resource across systems

**When to Use What:**

| Scenario | Use UUID4 | Use UUID5 |
|----------|-----------|----------|
| Primary keys in distributed DB | ✅ Yes | ❌ No |
| Non-guessable IDs | ✅ Yes | ❌ No |
| Need same ID for same input | ❌ No | ✅ Yes |
| Content-addressable storage | ❌ No | ✅ Yes |
| Random, unique identifiers | ✅ Yes | ❌ No |
| Deterministic generation needed | ❌ No | ✅ Yes |

### Integer Types & Ranges

**INT (32-bit signed integer):**
- **Size:** 4 bytes
- **Range:** -2,147,483,648 to 2,147,483,647
- **Power notation:** -2³¹ to 2³¹ - 1
- **Use cases:** Counters, IDs, quantities

**BIGINT (64-bit signed integer):**
- **Size:** 8 bytes
- **Range:** -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
- **Power notation:** -2⁶³ to 2⁶³ - 1
- **Use cases:** Large counters, timestamps (milliseconds since epoch)

**SMALLINT (16-bit signed integer):**
- **Size:** 2 bytes
- **Range:** -32,768 to 32,767
- **Power notation:** -2¹⁵ to 2¹⁵ - 1
- **Use cases:** Small quantities, status codes

### Content-Addressable Storage (CAS)

**What is Content-Addressable Storage?**

Content-Addressable Storage (CAS) is a storage mechanism where data is stored and retrieved based on **its content**, not its location or a pre-assigned identifier. The address/identifier is **derived from the content itself** using a cryptographic hash function.

**Key Concept:**
- **Traditional storage:** Location-based addressing (e.g., file path: `/users/john/document.txt`)
- **Content-addressable storage:** Content-based addressing (e.g., hash: `sha256:abc123...`)

**How It Works:**

1. **Content Hashing:**
   - Take the content (file, data, object)
   - Hash it using a cryptographic hash function (SHA-256, SHA-1, MD5)
   - The hash becomes the **address/identifier** for that content

2. **Storage:**
   - Store content using the hash as the key
   - Example: `hash(content) → content`

3. **Retrieval:**
   - To retrieve: provide the hash, system returns the content
   - If content doesn't exist, hash tells you immediately (no need to search)

**Example:**

```python
# Content-addressable storage example
import hashlib

# Step 1: Hash the content
content = b"This is my file content"
content_hash = hashlib.sha256(content).hexdigest()
# Result: "a3b5c7d9e1f2..." (64 hex characters)

# Step 2: Store using hash as key
storage[content_hash] = content

# Step 3: Retrieve using hash
retrieved_content = storage[content_hash]
# Returns: "This is my file content"

# Step 4: Check if content exists
if content_hash in storage:
    print("Content already stored - deduplication!")
```

**Key Properties:**

1. **Deterministic:**
   - Same content → same hash → same address
   - Content can be verified by re-hashing

2. **Deduplication:**
   - If two users upload the same file, they get the same hash
   - Only one copy needs to be stored
   - Saves storage space

3. **Integrity Verification:**
   - Can verify content hasn't changed by re-hashing
   - If hash matches, content is intact

4. **Location-Independent:**
   - Content can be stored anywhere
   - Hash uniquely identifies it regardless of location

**Real-World Examples:**

1. **Git (Version Control):**
   - Files stored by SHA-1 hash of their content
   - Commit hash identifies entire commit
   - Example: `git commit abc123def456...`

2. **Docker Images:**
   - Image layers stored by content hash
   - Same layer shared across multiple images
   - Example: `sha256:abc123...`

3. **IPFS (InterPlanetary File System):**
   - Files stored and retrieved by content hash
   - Distributed storage system
   - Example: `ipfs://QmHash...`

4. **Blockchain:**
   - Blocks identified by hash of their content
   - Each block's hash includes previous block's hash
   - Creates immutable chain

5. **Cloud Storage (S3, etc.):**
   - Can use content hashing for deduplication
   - Store files by hash, reference by hash

**Benefits:**

✅ **Automatic Deduplication:**
- Same content stored only once
- Saves storage space
- Example: 1000 users upload same image → stored once

✅ **Integrity Checking:**
- Verify content hasn't been corrupted
- Re-hash and compare with stored hash

✅ **Tamper Detection:**
- Any change to content changes the hash
- Easy to detect unauthorized modifications

✅ **Distributed Storage:**
- Content can be stored on any node
- Hash uniquely identifies it globally
- No need for centralized location registry

✅ **Efficient Lookups:**
- Direct hash lookup (O(1) complexity)
- No need to search through files

**Challenges:**

❌ **Hash Collisions:**
- Two different contents could theoretically produce same hash
- Very rare with good hash functions (SHA-256)
- Probability: ~1 in 2²⁵⁶

❌ **No Human-Readable Names:**
- Hashes are not user-friendly
- Need separate mapping: human name → hash

❌ **Content Modification:**
- Any change to content changes hash
- Old hash becomes invalid
- Need versioning strategy

**Use Cases:**

1. **File Storage Systems:**
   - Store files by content hash
   - Deduplicate automatically
   - Example: Dropbox, Google Drive (internal)

2. **Backup Systems:**
   - Store backups by content hash
   - Only store changed blocks
   - Example: rsync, backup software

3. **CDN (Content Delivery Network):**
   - Cache content by hash
   - Verify content integrity
   - Example: CloudFlare, AWS CloudFront

4. **Distributed Systems:**
   - Share content across nodes
   - Hash ensures consistency
   - Example: IPFS, distributed databases

5. **Version Control:**
   - Track file versions by hash
   - Detect changes automatically
   - Example: Git, Mercurial

**CAS vs Location-Based Storage:**

| Aspect | Location-Based | Content-Addressable |
|--------|----------------|---------------------|
| **Address** | Path/URL (e.g., `/files/doc.txt`) | Hash (e.g., `sha256:abc123...`) |
| **Deduplication** | Manual | Automatic |
| **Integrity** | Must verify separately | Built-in (re-hash to verify) |
| **Human-readable** | Yes | No (need mapping) |
| **Content changes** | Same address | New hash (new address) |
| **Lookup** | Path traversal | Direct hash lookup |
| **Distributed** | Requires location registry | Hash works globally |

**Implementation Example:**

```python
class ContentAddressableStorage:
    def __init__(self):
        self.storage = {}  # hash -> content
        self.name_to_hash = {}  # human name -> hash

    def store(self, content, name=None):
        # Hash the content
        content_hash = hashlib.sha256(content).hexdigest()

        # Check if already stored (deduplication)
        if content_hash in self.storage:
            print(f"Content already stored with hash: {content_hash}")
            if name:
                self.name_to_hash[name] = content_hash
            return content_hash

        # Store content
        self.storage[content_hash] = content
        if name:
            self.name_to_hash[name] = content_hash

        return content_hash

    def retrieve(self, hash_or_name):
        # If name provided, get hash
        if hash_or_name in self.name_to_hash:
            hash_key = self.name_to_hash[hash_or_name]
        else:
            hash_key = hash_or_name

        # Retrieve by hash
        return self.storage.get(hash_key)

    def verify(self, content, hash_key):
        # Verify content integrity
        computed_hash = hashlib.sha256(content).hexdigest()
        return computed_hash == hash_key

# Usage
cas = ContentAddressableStorage()

# Store file
hash1 = cas.store(b"Hello World", name="greeting.txt")
# Returns: "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"

# Store same content again (deduplication)
hash2 = cas.store(b"Hello World", name="hello.txt")
# Returns: Same hash (content already stored)

# Retrieve by hash
content = cas.retrieve(hash1)
# Returns: b"Hello World"

# Retrieve by name
content = cas.retrieve("greeting.txt")
# Returns: b"Hello World"

# Verify integrity
is_valid = cas.verify(b"Hello World", hash1)
# Returns: True
```

---

## Interview Tips

1. **Start with Requirements:** Always clarify functional and non-functional requirements first
2. **Think Out Loud:** Explain your reasoning as you design
3. **Ask Questions:** Don't assume - clarify constraints and requirements
4. **Start Simple:** Begin with basic design, then add complexity
5. **Consider Trade-offs:** Discuss pros/cons of design decisions
6. **Scale Gradually:** Start with single server, then scale out
7. **Use BTSM:** Always cover Bandwidth, Traffic, Storage, Memory
8. **Draw Diagrams:** Visual representation helps communication
9. **Discuss Failure Cases:** What happens when components fail?
10. **Time Management:** Allocate time wisely across sections

---

## Common System Design Patterns

1. **Load Balancing:** Distribute traffic across servers
2. **Caching:** Reduce latency and database load
3. **Database Replication:** Read replicas for scaling reads
4. **Sharding:** Partition data across multiple databases
5. **CDN:** Distribute content globally
6. **Message Queues:** Decouple components, handle async processing
7. **Rate Limiting:** Prevent abuse, ensure fair usage
8. **Circuit Breaker:** Prevent cascading failures

---

## Practice Problems

1. URL Shortener (TinyURL) - Easy
2. Pastebin - Easy
3. Instagram - Medium
4. Twitter - Medium
5. Facebook News Feed - Medium
6. Facebook Messenger - Medium (see `FACEBOOK_MESSENGER_EXAMPLE.md`)
7. WhatsApp - Medium
8. YouTube - Hard
9. Uber - Hard
10. Netflix - Hard
11. Google Drive - Hard

---

## Resources

- System Design Primer: https://github.com/donnemartin/system-design-primer
- High Scalability: http://highscalability.com/
- AWS Architecture Center: https://aws.amazon.com/architecture/

---

**Remember:** The goal is not to design the perfect system, but to demonstrate:
- Problem-solving approach
- Trade-off analysis
- Scalability thinking
- Communication skills

Good luck with your interviews! 🚀
