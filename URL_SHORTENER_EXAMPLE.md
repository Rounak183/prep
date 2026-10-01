# URL Shortener System Design - Detailed Example

This document provides a complete walkthrough of designing a URL shortening service (like TinyURL) with detailed explanations of all calculations and design decisions.

---

## Step 1: Problem Understanding & Requirements Clarification

### 1.1 Problem Statement
Design a URL shortening service like TinyURL that creates short aliases for long URLs.

**What it does:**
- Takes a long URL (e.g., `https://www.example.com/very/long/path/to/resource`)
- Generates a short alias (e.g., `http://tinyurl.com/abc123`)
- Redirects users to the original URL when they access the short link

**Similar services:** bit.ly, goo.gl, qlink.me, short.link

**Difficulty Level:** Easy

### 1.2 Functional Requirements
1. Given a URL, generate a shorter and unique alias (short link)
2. When users access a short link, redirect to the original URL
3. Users can optionally pick a custom short link
4. Links expire after a default timespan; users can specify expiration time

### 1.3 Non-Functional Requirements
1. **Highly available:** If service is down, all redirections fail (critical requirement)
2. **Real-time redirection:** URL redirection should happen in real-time with minimal latency
3. **Non-guessable:** Shortened links should not be predictable

### 1.4 Extended Requirements (Optional)
1. Analytics: Track how many times a redirection happened
2. REST APIs for other services to integrate

---

## Step 2: Capacity Estimation (BTSM Framework)

### 2.1 Traffic Estimation

**Read/Write Ratio:** 100:1 (read-heavy system)
- Most URLs are read (redirected) many times
- Few URLs are created compared to how often they're accessed

**Assumptions:**
- 500 million new URL shortenings per month
- 100:1 read/write ratio

**Calculations:**

**Quick Calculation Tip for Interviews:**
- **Exact:** 30 days × 24 hours × 3600 seconds = **2,592,000 seconds**
- **For quick mental math:** Round to **2.5 million seconds** (easier to divide)
  - Example: 500M / 2.5M = 200/s (close enough for interviews!)
  - The exact calculation gives ~193/s, but 200/s is fine for capacity planning

**Write QPS (Queries Per Second):**
```
500 million URLs / (30 days × 24 hours × 3600 seconds)
= 500,000,000 / (30 × 24 × 3600)
= 500,000,000 / 2,592,000
≈ 193 URLs/second
≈ 200 URLs/s (rounded)

Quick method: 500M / 2.5M = 200/s ✅
```

**Read QPS:**
```
Write QPS × Read/Write Ratio
= 200 × 100
= 20,000 redirects/second
= 20K/s
```

### 2.2 Storage Estimation

**Total Objects:**
```
500M URLs/month × 5 years × 12 months/year
= 500M × 60
= 30 billion URLs
```

**Size per Object: ~500 bytes**

**Detailed Byte Breakdown:**

#### How is Hash 7 bytes?
- We use **Base62 encoding** (a-z, A-Z, 0-9 = 62 characters)
- Short URL hash is **7 characters** (e.g., "abc1234")
- Each character in Base62 is stored as **1 byte** in UTF-8/ASCII
- **Calculation:** 7 characters × 1 byte/character = **7 bytes**

**Why 7 characters?**
- 62^7 = 3,521,614,606,208 (≈3.5 trillion unique combinations)
- This is more than enough for our use case (30 billion URLs)

#### How is Original URL 200-500 bytes?
- URLs can vary significantly in length
- **Maximum:** VARCHAR(2048) allows up to 2048 bytes
- **Average:** Most real-world URLs are much shorter
  - Short URL: `https://example.com` = ~20 bytes
  - Medium URL: `https://www.example.com/path/to/resource?param=value` = ~60-80 bytes
  - Long URL: `https://www.example.com/very/long/path/with/many/segments?param1=value1&param2=value2` = ~150-300 bytes
  - Very long URL (with query params, fragments): up to 500+ bytes

**Conservative estimate:**
- We assume average URL length is **200-500 bytes**
- This accounts for:
  - Protocol (`https://`) = 8 bytes
  - Domain name = 20-50 bytes
  - Path segments = 50-200 bytes
  - Query parameters = 50-200 bytes
  - Fragments = 0-50 bytes

**For calculation:** We use **~300 bytes** as average (middle of range)

#### Is Timestamp 8 bytes? (Yes, each datetime is 8 bytes)
- **TIMESTAMP** or **DATETIME** in most databases is stored as **8 bytes**
- This typically stores:
  - Date: Year, Month, Day
  - Time: Hour, Minute, Second, Microseconds
  - Timezone information (in some databases)

**Examples:**
- MySQL TIMESTAMP: 4 bytes (Unix timestamp) or 8 bytes (DATETIME)
- PostgreSQL TIMESTAMP: 8 bytes
- SQL Server DATETIME2: 6-8 bytes depending on precision

**For our calculation:**
- `created_at`: 8 bytes
- `expires_at`: 8 bytes
- **Total: 16 bytes** (2 timestamps × 8 bytes each)

#### How is User/API Key 100 bytes?
Actually, this is a **combination** of two fields:
- `user_id`: VARCHAR(50) = ~50 bytes
  - Example: "user_12345678901234567890" = ~30-50 bytes
- `api_dev_key`: VARCHAR(50) = ~50 bytes
  - Example: "api_key_abc123def456ghi789" = ~30-50 bytes

**Total: ~50 + 50 = ~100 bytes**

**Note:** In practice, these might be shorter (UUIDs are 36 bytes, shorter IDs are 10-20 bytes), but we use 50 bytes each to be conservative and account for variable lengths.

#### Click Count is Integer = 4 bytes? (Yes, exactly!)
- **INT** in most databases is **4 bytes** (32 bits)
- INT can store values from **-2,147,483,648 to 2,147,483,647**
- **In power terms:** -2,147,483,648 = **-2³¹** (negative 2 to the power of 31)
- Maximum value: 2,147,483,647 = **2³¹ - 1** (2 to the power of 31, minus 1)
- **Why these limits?** 32-bit signed integer uses 1 bit for sign, 31 bits for value
- For click counts, this is more than sufficient (over 2 billion clicks per URL!)
- **Calculation:** 4 bytes

**Alternative:** If we need larger numbers, we could use BIGINT (8 bytes = 64 bits), which can store up to **2⁶³ - 1** = 9,223,372,036,854,775,807, but INT is sufficient for most use cases.

#### How is Metadata 100 bytes?
**Metadata overhead** includes database internal structures:

1. **Row Header:** ~20-30 bytes
   - Stores row metadata, null bitmaps, row version info

2. **Null Bitmap:** ~5-10 bytes
   - Tracks which columns are NULL
   - 1 bit per nullable column

3. **Variable-length Column Overhead:** ~10-20 bytes
   - For VARCHAR columns, stores length information
   - Each variable-length column needs 2-4 bytes for length

4. **Index Overhead:** ~20-30 bytes
   - Primary key index entries
   - Additional indexes if any

5. **Padding/Alignment:** ~10-20 bytes
   - Data alignment for performance
   - Some databases pad rows to specific boundaries

6. **Page Header Overhead (proportional):** ~5-10 bytes
   - Distributed across rows on a page

**Total: ~100-150 bytes per row**

**For calculation:** We use **~100 bytes** as a conservative estimate.

#### Complete Storage Calculation:

**Field-by-field breakdown:**
```
hash (short URL):           7 bytes
original_url (average):   300 bytes  (200-500 range, using 300 as average)
created_at:                 8 bytes
expires_at:                 8 bytes
user_id:                   50 bytes
api_dev_key:               50 bytes
click_count:                4 bytes
metadata overhead:        100 bytes
────────────────────────────────────
Total:                    527 bytes
```

**Conservative estimate: ~500 bytes per object**
- We round to 500 bytes to account for:
  - Variable URL lengths (some shorter, some longer)
  - Database compression (if enabled, reduces size)
  - Actual metadata might be less in some databases

**Total Storage:**
```
30 billion URLs × 500 bytes
= 30,000,000,000 × 500
= 15,000,000,000,000 bytes
= 15 TB (Terabytes)
```

### 2.3 Bandwidth Estimation

**Incoming Data (Write):**
```
200 URLs/s × 500 bytes
= 100,000 bytes/second
= 100 KB/s
```

**Outgoing Data (Read):**
```
20,000 redirects/s × 500 bytes
= 10,000,000 bytes/second
= 10 MB/s
```

**Note:** For redirects, we might only send the original URL (not the full row), so actual outgoing bandwidth might be less. But for capacity planning, we use the full object size.

### 2.4 Memory (Cache) Estimation

**Strategy:** Cache 20% of hot URLs (80-20 rule)
- 20% of URLs generate 80% of traffic
- Cache the frequently accessed URLs

**Daily Requests:**
```
20K redirects/s × 3600 seconds/hour × 24 hours/day
= 20,000 × 3,600 × 24
= 1,728,000,000 requests/day
≈ 1.7 billion requests/day
```

**Cache Size:**
```
20% of daily requests × 500 bytes
= 0.2 × 1.7 billion × 500 bytes
= 340,000,000,000 bytes
= 340 GB
≈ 170 GB (after accounting for duplicate requests)
```

**Note:** Actual cache usage is less because:
- Same URL is requested multiple times (we only cache it once)
- Cache hit rate reduces the number of unique URLs we need to cache
- We might cache only the original URL (not full row), reducing size

### 2.5 Summary Table

| Metric | Value | Calculation |
|--------|-------|-------------|
| Write QPS | 200/s | 500M / (30×24×3600) |
| Read QPS | 20K/s | 200 × 100 |
| Incoming Data | 100 KB/s | 200/s × 500 bytes |
| Outgoing Data | 10 MB/s | 20K/s × 500 bytes |
| Storage (5 years) | 15TB | 30B × 500 bytes |
| Memory for Cache | 170GB | 0.2 × 1.7B × 500 bytes |

---

## Common Data Types Reference

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

**UUID Versions:**

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

**OID Example:**
```
OID: 1.3.6.1.4.1.12345.1.2.3
Meaning:
- 1.3.6.1.4.1 = Private enterprise
- 12345 = Company/Organization ID
- 1.2.3 = Specific object within that organization
```

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

# More complex example
CN=Jane Smith,OU=Sales,OU=North America,O=Acme Corp,L=New York,ST=NY,C=US
```

**DN Characteristics:**
- **Unique:** Each DN uniquely identifies one entry in the directory
- **Hierarchical:** Reflects the directory tree structure
- **Readable:** Human-readable format (unlike OIDs)
- **Order matters:** Most specific first, then more general

**X.500 and LDAP:**
- **X.500:** Original directory service standard (1980s)
- **LDAP:** Lightweight version of X.500 (simpler, more widely used)
- Both use DNs to identify entries
- LDAP is the modern standard (Active Directory, OpenLDAP, etc.)

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

**Why These Namespaces Exist:**
- **DNS namespace:** For domain names (internet infrastructure)
- **URL namespace:** For web URLs (web resources)
- **OID namespace:** For object identifiers (directory schemas, SNMP, etc.)
- **X.500 DN namespace:** For distinguished names (LDAP, directory services)

**Real-World Example:**
```
# Generate UUID5 from OID
OID: 1.3.6.1.4.1.12345
Namespace: OID namespace UUID
Result: Deterministic UUID for that OID

# Generate UUID5 from DN
DN: CN=John Doe,OU=Engineering,O=Acme Corp,C=US
Namespace: X.500 DN namespace UUID
Result: Deterministic UUID for that DN
```

**For URL Shortener Context:**
- You typically use **URL namespace** for generating UUIDs from URLs
- OID and DN namespaces are more relevant for:
  - Enterprise directory systems
  - LDAP-based authentication
  - Certificate management
  - Network management (SNMP)

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

**Note:** You're correct! The version is in the **7th byte** (1-indexed). The bits are:
- **Bits 48-51** of the entire UUID (bits 0-3 of byte 7)
- These correspond to **bits 12-15** when counting within the time_hi_and_version field

**UUID Byte Structure:**
```
UUID: xxxxxxxx-xxxx-Vxxx-xxxx-xxxxxxxxxxxx
      └───┬──┘└─┬─┘ └─┬─┘ └─┬─┘ └─────┬─────┘
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

**Bit Numbering Examples:**
```
UUID: 550e8400-e29b-41d4-a716-446655440000
      └───┬───┘ └─┬─┘ └─┬─┘ └─┬─┘ └─────┬─────┘
         Bits    Bits  Bits  Bits      Bits
         0-31    32-47 48-63 64-79     80-127
                  │     │
                  │     └─ Version is here (bits 48-51)
                  └─────── time_mid
```

**Example:**
```
UUID: 550e8400-e29b-41d4-a716-446655440000
      └───┬───┘ └─┬─┘ └─┬─┘ └─┬─┘ └─────┬─────┘
         Bytes    Bytes  Bytes  Bytes    Bytes
         1-4      5-6    7-8    9-10     11-16
                  │      │
                  │      └─ "41d4" = bytes 7-8
                  │         Byte 7 = 0x41 = 0100 0001
                  │         Bits 48-51 = 0100 = version 4
                  └──────── "e29b" = bytes 5-6
```

**Note:** You're correct! The version bits are in the **7th byte** (1-indexed) or **byte 6** (0-indexed), specifically in bits 48-51 (the 4 most significant bits of that byte).

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
- **Within time_hi_and_version field:** Version bits are bits 48-51
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

**Your Understanding is Correct!**

Yes, you've got it right! Here's the complete process:

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

**For URL Shortener:**
- **UUID4:** Could use for `user_id` or `api_dev_key` (non-sequential, secure)
- **UUID5:** Not typically used (we use Base62 hash for short URLs instead)
- **Alternative:** Use Base62 hash (7 chars) for short URLs, UUID for user IDs

### Integer Types

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

**For URL Shortener Context:**

While URL shorteners typically use location-based storage (hash → original URL), CAS concepts can be applied for:
- **Deduplication:** If same URL is shortened multiple times, could use content hash
- **Integrity:** Verify stored URLs haven't been tampered with
- **Analytics:** Hash click events by content for deduplication

However, URL shorteners usually prefer location-based (hash → URL) because:
- Need human-readable short URLs
- URLs are unique per user (even if same destination)
- Need to track individual short URL usage

---

## Step 3: System APIs

### 3.1 Create Short URL (POST)
**Endpoint:** `POST /api/v1/shorten`

**Request Headers:**
- `Authorization: Bearer {api_dev_key}` (Required)
- `Content-Type: application/json`

**Request Body:**
```json
{
  "original_url": "https://www.example.com/very/long/url",
  "custom_alias": "my-custom-link",  // Optional
  "expiration_date": "2025-12-31T23:59:59Z"  // Optional, ISO 8601 format
}
```

**Success Response (201 Created):**
```json
{
  "short_url": "http://tinyurl.com/abc123",
  "short_alias": "abc123",
  "original_url": "https://www.example.com/very/long/url",
  "expires_at": "2025-12-31T23:59:59Z",
  "created_at": "2025-01-15T10:30:00Z"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid URL format, invalid expiration date
- `401 Unauthorized`: Missing or invalid api_dev_key
- `403 Forbidden`: Insufficient permissions (not authorized to create URLs)
- `409 Conflict`: Custom alias already in use
- `429 Too Many Requests`: Rate limit exceeded, quota exceeded
- `500 Internal Server Error`: Server error

### 3.2 Get Original URL (GET)
**Endpoint:** `GET /api/v1/{short_alias}`

**Path Parameters:**
- `short_alias`: The short URL alias (e.g., "abc123")

**Success Response (200 OK):**
```json
{
  "original_url": "https://www.example.com/very/long/url",
  "status": "active",  // "active" | "expired" | "deleted"
  "created_at": "2025-01-15T10:30:00Z",
  "expires_at": "2025-12-31T23:59:59Z",
  "click_count": 1250
}
```

**For Browser Redirects:**
- `302 Found`: Redirect to original URL (with `Location` header)
- `410 Gone`: URL expired/deleted (show error page)

**Error Responses:**
- `404 Not Found`: Short alias does not exist
- `410 Gone`: URL has expired or been deleted
- `500 Internal Server Error`: Server error

### 3.3 Update Short URL (PUT)
**Endpoint:** `PUT /api/v1/{short_alias}`

**Request Headers:**
- `Authorization: Bearer {api_dev_key}` (Required)
- `Content-Type: application/json`

**Request Body:**
```json
{
  "original_url": "https://www.example.com/new/updated/url",  // Optional
  "expiration_date": "2026-12-31T23:59:59Z"  // Optional
}
```

**Success Response (200 OK):**
```json
{
  "short_url": "http://tinyurl.com/abc123",
  "original_url": "https://www.example.com/new/updated/url",
  "expires_at": "2026-12-31T23:59:59Z",
  "updated_at": "2025-01-20T15:45:00Z"
}
```

**Note:** PUT returns `200 OK` (not 201) because it updates an existing resource, not creates a new one.

### 3.4 Delete Short URL (DELETE)
**Endpoint:** `DELETE /api/v1/{short_alias}`

**Request Headers:**
- `Authorization: Bearer {api_dev_key}` (Required)

**Success Response (204 No Content):**
- No response body (resource successfully deleted)
- Or `200 OK` with body if you want to return metadata:

```json
{
  "status": "deleted",
  "message": "URL successfully deleted",
  "deleted_at": "2025-01-20T16:00:00Z"
}
```

**Note:** `204 No Content` is more RESTful (no body needed), but `200 OK` with body is also acceptable if you want to return metadata.

### 3.5 Get Analytics (GET)
**Endpoint:** `GET /api/v1/{short_alias}/analytics`

**Request Headers:**
- `Authorization: Bearer {api_dev_key}` (Required)

**Query Parameters:**
- `start_date`: Optional (ISO 8601 format)
- `end_date`: Optional (ISO 8601 format)

**What is ISO 8601 Format?**
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

**Common Formats:**
- **Date:** `2025-01-15`
- **DateTime (UTC):** `2025-01-15T10:30:00Z`
- **DateTime (with timezone):** `2025-01-15T10:30:00+05:30`
- **DateTime (with milliseconds):** `2025-01-15T10:30:00.123Z`

**Examples in Different Languages:**
```python
# Python
from datetime import datetime
datetime.now().isoformat()
# Result: "2025-01-15T10:30:00.123456"

# JavaScript
new Date().toISOString()
# Result: "2025-01-15T10:30:00.123Z"

# API Request
GET /api/v1/analytics?start_date=2025-01-15T00:00:00Z&end_date=2025-01-15T23:59:59Z
```

**Success Response (200 OK):**
```json
{
  "short_alias": "abc123",
  "total_clicks": 1250,
  "unique_visitors": 980,
  "clicks_by_date": [
    {"date": "2025-01-15", "clicks": 50},
    {"date": "2025-01-16", "clicks": 75}
  ],
  "top_referrers": [
    {"source": "google.com", "clicks": 500},
    {"source": "twitter.com", "clicks": 300}
  ],
  "geographic_distribution": [
    {"country": "US", "clicks": 600},
    {"country": "UK", "clicks": 200}
  ]
}
```

### 3.6 Abuse Prevention & Rate Limiting

**Rate Limiting Strategy:**
- Each `api_dev_key` has a quota:
  - **Free tier:** 100 URL creations/day, 10K redirections/day
  - **Paid tier:** 10K URL creations/day, 1M redirections/day
  - **Enterprise:** Custom limits

**Rate Limit Headers:**
These headers are added to **every response** (both success and error) to inform clients about rate limits:

```
X-RateLimit-Limit: 100          // Total requests allowed in time window
X-RateLimit-Remaining: 45         // Requests remaining in current window
X-RateLimit-Reset: 1640995200    // Unix timestamp when limit resets
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

**How Rate Limit Headers Work:**
1. **Server-side:** Before processing request, check rate limit counter (stored in Redis)
2. **If under limit:** Process request, decrement counter, add headers to response
3. **If over limit:** Return `429 Too Many Requests` with headers showing limit exceeded
4. **Headers added:** In response middleware/filter, regardless of success/error

**Implementation Example:**
```python
# Pseudo-code
def rate_limit_middleware(request):
    api_key = request.headers['Authorization']
    limit = get_rate_limit(api_key)  # e.g., 100/day

    # Check Redis counter
    current_count = redis.get(f"rate_limit:{api_key}:{date}")

    # Add headers to response
    response.headers['X-RateLimit-Limit'] = limit
    response.headers['X-RateLimit-Remaining'] = max(0, limit - current_count)
    response.headers['X-RateLimit-Reset'] = get_reset_timestamp()

    if current_count >= limit:
        return 429, response  # Too Many Requests
    else:
        redis.incr(f"rate_limit:{api_key}:{date}")
        return process_request(request)
```

**Additional Abuse Prevention:**
1. **URL Validation:** Check for malicious URLs, spam patterns
2. **IP-based Rate Limiting:** Limit requests per IP address
3. **Custom Alias Validation:** Prevent reserved/system aliases
4. **Monitoring:** Track suspicious patterns (e.g., rapid creation/deletion)

---

## Step 4: Database Design

### 4.1 Observations About the Data

**Key characteristics:**
1. **Billions of records:** 30 billion URLs over 5 years
2. **Small objects:** Each record is <1KB (~500 bytes average)
3. **Minimal relationships:** Only one relationship - User to URLs (one-to-many)
4. **Read-heavy:** 100:1 read/write ratio (20K reads/s vs 200 writes/s)
5. **Simple access pattern:** Primary operation is key-value lookup by short URL hash
6. **Two main tables:** URL table (billions of rows) and User table (millions of rows)

### 4.2 Data Models

**URL Mapping Table (Key-Value Store):**

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
  "hash": "abc123",                    // Partition key (short URL hash)
  "original_url": "https://example.com/very/long/url",
  "created_at": "2025-01-15T10:30:00Z",
  "expires_at": "2025-12-31T23:59:59Z",
  "user_id": "user_12345",             // Optional
  "api_dev_key": "api_key_abc",        // Optional
  "click_count": 1250
}
```

**Why JSON for Document Databases?**
- Document databases store data as documents (JSON-like structures)
- JSON is human-readable and easy to understand
- Matches how data is stored and retrieved
- Works well for nested/hierarchical data

**Column-Family Schema (Cassandra) - Different Format:**
```
Table: urls
Partition Key: hash
Clustering Columns: created_at

Column Family Structure:
hash (partition key) | created_at | original_url | user_id | click_count
---------------------|------------|--------------|---------|-------------
abc123              | 2025-01-15 | https://...  | user_1  | 1250
def456              | 2025-01-16 | https://...  | user_2  | 500
```

**Key-Value Store Schema (Redis/Riak) - Simple Format:**
```
Key: "url:abc123"
Value: {
  "original_url": "https://example.com/very/long/url",
  "created_at": "2025-01-15T10:30:00Z",
  "user_id": "user_12345",
  "click_count": 1250
}
```

**Graph Database Schema (Neo4j) - Node/Relationship Format:**
```
Node: User
  Properties: {user_id: "user_12345", name: "John"}

Node: URL
  Properties: {hash: "abc123", original_url: "https://..."}

Relationship: CREATED
  From: User
  To: URL
  Properties: {created_at: "2025-01-15T10:30:00Z"}
```

**For URL Shortener (DynamoDB/Cassandra/Riak):**

Since we're using **key-value stores** (DynamoDB, Cassandra, Riak), we typically represent the schema as:

**DynamoDB (Document/Key-Value):**
- ✅ JSON format (as shown above)
- Each item is a JSON document
- Partition key: `hash`

**Cassandra (Column-Family):**
- ⚠️ Column-family structure (not pure JSON)
- But often described in JSON for clarity in documentation
- Partition key: `hash`
- Clustering columns: `created_at` (optional)

**Riak (Key-Value):**
- ✅ JSON format (value is JSON)
- Key: `url:{hash}`
- Value: JSON document

**Summary:**
- **Document/Key-Value databases:** Often use JSON representation ✅
- **Column-Family databases:** Use column-family structure, but JSON is common in docs ⚠️
- **Graph databases:** Use node/relationship structure ❌
- **In practice:** JSON is commonly used in documentation for clarity, even for non-JSON databases

**Alternative SQL Schema (if using SQL):**

**Simplified Two-Table Design:**
```sql
-- URL Table
CREATE TABLE URL (
    Hash VARCHAR(16) PRIMARY KEY,          -- Short URL hash (Base62, 7-16 chars)
    OriginalURL VARCHAR(512) NOT NULL,     -- Original long URL
    CreationDate DATETIME NOT NULL,        -- When short URL was created
    ExpirationDate DATETIME,               -- When short URL expires
    UserID INT,                            -- Foreign key to User table
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    INDEX idx_user_id (UserID),            -- Index for user queries
    INDEX idx_expiration_date (ExpirationDate)  -- Index for cleanup jobs
    -- See detailed explanation of indexes below
);

-- User Table
CREATE TABLE User (
    UserID INT PRIMARY KEY AUTO_INCREMENT, -- User identifier
    Name VARCHAR(20),                      -- User's name
    Email VARCHAR(32) UNIQUE,              -- User's email
    CreationDate DATETIME NOT NULL,        -- When user account was created
    LastLogin DATETIME                     -- Last login timestamp
);
```

**Relationship:**
- One User can create many URLs (one-to-many relationship)
- `UserID` in URL table references `UserID` in User table
- Foreign key ensures referential integrity

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
1. **Insert Rule:** Can't insert a URL with UserID=999 if UserID=999 doesn't exist in User table
2. **Update Rule:** Can't update User.UserID if URLs reference that UserID (unless CASCADE)
3. **Delete Rule:** Can't delete a User if URLs reference that User (unless CASCADE or SET NULL)

**Example of Referential Integrity:**
```sql
-- This will FAIL (referential integrity violation):
INSERT INTO URL (Hash, UserID) VALUES ('abc123', 999);
-- Error: Foreign key constraint fails - UserID 999 doesn't exist

-- This will SUCCEED:
INSERT INTO User (UserID, Name) VALUES (999, 'John');
INSERT INTO URL (Hash, UserID) VALUES ('abc123', 999);
-- OK: UserID 999 exists in User table

-- This will FAIL (can't delete referenced user):
DELETE FROM User WHERE UserID = 999;
-- Error: Foreign key constraint fails - URLs still reference this user
```

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

**Example Schema with Cascading:**

```sql
-- User table (parent)
CREATE TABLE User (
    UserID INT PRIMARY KEY,
    Name VARCHAR(20)
);

-- URL table (child) with CASCADE
CREATE TABLE URL (
    Hash VARCHAR(16) PRIMARY KEY,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
        ON DELETE CASCADE      -- Delete URLs when User is deleted
        ON UPDATE CASCADE      -- Update UserID in URLs when User.UserID changes
);
```

**CASCADE Examples:**

**1. ON DELETE CASCADE:**
```sql
-- Insert data
INSERT INTO User (UserID, Name) VALUES (123, 'John');
INSERT INTO URL (Hash, UserID) VALUES ('abc123', 123);
INSERT INTO URL (Hash, UserID) VALUES ('def456', 123);
INSERT INTO URL (Hash, UserID) VALUES ('ghi789', 123);

-- Delete user with CASCADE
DELETE FROM User WHERE UserID = 123;

-- Result:
-- ✅ User 123 is deleted
-- ✅ All URLs with UserID=123 are automatically deleted
-- No orphaned URLs remain
```

**2. ON UPDATE CASCADE:**
```sql
-- Insert data
INSERT INTO User (UserID, Name) VALUES (123, 'John');
INSERT INTO URL (Hash, UserID) VALUES ('abc123', 123);

-- Update user ID with CASCADE
UPDATE User SET UserID = 999 WHERE UserID = 123;

-- Result:
-- ✅ User.UserID changed from 123 to 999
-- ✅ URL.UserID automatically updated from 123 to 999
-- URL still references the same user
```

**3. SET NULL:**
```sql
-- URL table with SET NULL
CREATE TABLE URL (
    Hash VARCHAR(16) PRIMARY KEY,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
        ON DELETE SET NULL    -- Set UserID to NULL when User is deleted
        ON UPDATE CASCADE
);

-- Delete user with SET NULL
DELETE FROM User WHERE UserID = 123;

-- Result:
-- ✅ User 123 is deleted
-- ✅ All URLs with UserID=123 have UserID set to NULL
-- URLs remain but are "orphaned" (no user reference)
```

**4. SET DEFAULT:**
```sql
-- URL table with SET DEFAULT
CREATE TABLE URL (
    Hash VARCHAR(16) PRIMARY KEY,
    UserID INT DEFAULT 0,  -- Default value
    FOREIGN KEY (UserID) REFERENCES User(UserID)
        ON DELETE SET DEFAULT    -- Set UserID to 0 when User is deleted
        ON UPDATE CASCADE
);

-- Delete user with SET DEFAULT
DELETE FROM User WHERE UserID = 123;

-- Result:
-- ✅ User 123 is deleted
-- ✅ All URLs with UserID=123 have UserID set to 0 (default)
-- URLs remain with default UserID value
```

**5. RESTRICT/NO ACTION (Default):**
```sql
-- URL table with RESTRICT (default behavior)
CREATE TABLE URL (
    Hash VARCHAR(16) PRIMARY KEY,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
        ON DELETE RESTRICT    -- Prevent deletion if URLs exist
        ON UPDATE RESTRICT
);

-- Try to delete user with RESTRICT
DELETE FROM User WHERE UserID = 123;

-- Result:
-- ❌ ERROR: Cannot delete User 123 because URLs reference it
-- ✅ User is NOT deleted
-- ✅ URLs remain unchanged
-- Must delete URLs first, then User
```

**Complete Example with All Options:**

```sql
-- Create tables with different cascade options
CREATE TABLE User (
    UserID INT PRIMARY KEY,
    Name VARCHAR(20)
);

-- Option 1: CASCADE (delete/update children automatically)
CREATE TABLE URL_CASCADE (
    Hash VARCHAR(16) PRIMARY KEY,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Option 2: SET NULL (set to NULL when parent deleted)
CREATE TABLE URL_SET_NULL (
    Hash VARCHAR(16) PRIMARY KEY,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- Option 3: RESTRICT (prevent deletion)
CREATE TABLE URL_RESTRICT (
    Hash VARCHAR(16) PRIMARY KEY,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT
);

-- Insert test data
INSERT INTO User (UserID, Name) VALUES (123, 'John');
INSERT INTO URL_CASCADE (Hash, UserID) VALUES ('abc1', 123);
INSERT INTO URL_SET_NULL (Hash, UserID) VALUES ('abc2', 123);
INSERT INTO URL_RESTRICT (Hash, UserID) VALUES ('abc3', 123);

-- Test DELETE with CASCADE
DELETE FROM User WHERE UserID = 123;
-- Result:
-- ✅ User deleted
-- ✅ URL_CASCADE deleted (CASCADE)
-- ✅ URL_SET_NULL.UserID = NULL (SET NULL)
-- ❌ URL_RESTRICT prevents deletion (RESTRICT) - User still exists
```

**When to Use Each Option:**

**CASCADE:**
- ✅ Use when: Child records have no meaning without parent
- ✅ Example: URLs belong to user, delete user → delete URLs
- ⚠️ Warning: Can delete many records unintentionally

**SET NULL:**
- ✅ Use when: Child records can exist independently
- ✅ Example: URLs can exist without user (anonymous URLs)
- ⚠️ Warning: Creates orphaned records (need to handle NULL)

**SET DEFAULT:**
- ✅ Use when: Child records should have a default parent
- ✅ Example: URLs default to "system" user when user deleted
- ⚠️ Warning: Default value must exist in parent table

**RESTRICT/NO ACTION:**
- ✅ Use when: Child records must always have valid parent
- ✅ Example: Financial transactions must always have valid account
- ✅ Default behavior (safest option)

**For URL Shortener:**

**Recommended Approach:**
```sql
CREATE TABLE URL (
    Hash VARCHAR(16) PRIMARY KEY,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
        ON DELETE SET NULL    -- URLs can exist without user (anonymous)
        ON UPDATE CASCADE     -- Update UserID if user ID changes
);
```

**Why SET NULL for DELETE:**
- URLs might be shared/used even if user account is deleted
- Preserves URL functionality
- Can later reassign to different user if needed

**Why CASCADE for UPDATE:**
- If UserID changes, URLs should reference new ID
- Maintains referential integrity
- Rare operation (user IDs usually don't change)

**Alternative Extended SQL Schema (with more fields):**
```sql
CREATE TABLE urls (
    hash VARCHAR(7) PRIMARY KEY,           -- Short URL hash (Base62, 7 chars)
    original_url VARCHAR(2048) NOT NULL,    -- Original long URL
    created_at TIMESTAMP NOT NULL,          -- Creation timestamp
    expires_at TIMESTAMP,                   -- Expiration timestamp
    user_id INT,                            -- Foreign key to users table
    api_dev_key VARCHAR(50),                -- API key used (optional)
    click_count INT DEFAULT 0,             -- Number of clicks
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id),            -- Index for user queries
    INDEX idx_expires_at (expires_at)       -- Index for expiration cleanup
);

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20),
    email VARCHAR(32) UNIQUE,
    api_dev_key VARCHAR(50) UNIQUE,
    created_at TIMESTAMP,
    last_login TIMESTAMP,
    tier VARCHAR(20) DEFAULT 'free'  -- free, paid, enterprise
);
```

**User Table (NoSQL):**
```json
// NoSQL
{
  "user_id": "user_12345",
  "email": "user@example.com",
  "api_dev_key": "api_key_abc",
  "created_at": "2025-01-01T00:00:00Z",
  "tier": "free"  // free, paid, enterprise
}
```

### 4.3 Database Choice: NoSQL vs SQL

**Recommended: NoSQL Key-Value Store**

**Why NoSQL (DynamoDB, Cassandra, Riak) is Better:**

✅ **Billions of records:**
- NoSQL databases are designed for horizontal scaling
- Easier to shard and distribute across multiple nodes
- SQL databases can struggle with billions of rows

✅ **Small objects (<1KB):**
- Key-value stores are optimized for small, simple records
- Perfect fit for URL mappings (hash → original_url)

✅ **Minimal relationships:**
- Only one relationship: User to URLs (one-to-many)
- We don't need complex joins for most queries
- Simple key-value lookups are NoSQL's strength
- User-URL relationship can be denormalized (store user_id in URL record)

**What is Denormalization?**

**Denormalization** is the process of intentionally adding redundant data to improve read performance, at the cost of some data duplication and potential inconsistency.

**Normalized vs Denormalized:**

**Normalized (SQL approach):**
```sql
-- Separate tables with foreign keys
User Table:
  UserID | Name | Email
  -------|------|-------
  123    | John | john@example.com

URL Table:
  Hash   | OriginalURL | UserID (foreign key)
  -------|-------------|-------
  abc123 | https://... | 123
  def456 | https://... | 123
```

**Denormalized (NoSQL approach):**
```json
// Store user info directly in URL record (redundant but faster)
{
  "hash": "abc123",
  "original_url": "https://...",
  "user_id": "123",
  "user_name": "John",        // Denormalized - duplicated from User table
  "user_email": "john@example.com"  // Denormalized - duplicated
}
```

**Why Denormalize?**

✅ **Faster Reads:**
- No JOINs needed - all data in one record
- Single query instead of multiple queries
- Example: Get URL + user info in one read

✅ **Better for NoSQL:**
- NoSQL doesn't support JOINs efficiently
- Denormalization is the NoSQL way

✅ **Reduced Latency:**
- Fewer database round trips
- All data in one place

**Trade-offs:**

⚠️ **Data Duplication:**
- User info stored in every URL record
- More storage space needed

⚠️ **Update Complexity:**
- If user name changes, must update all URL records
- Or accept eventual consistency (user name might be stale in some URLs)

⚠️ **Potential Inconsistency:**
- User name in URL record might not match User table
- Acceptable if eventual consistency is OK

**For URL Shortener:**
- Store `user_id` in URL record (minimal denormalization)
- Don't store full user info (to avoid update complexity)
- If needed, can fetch user info separately (rare operation)

✅ **Read-heavy workload:**
- NoSQL can handle high read throughput
- Cassandra/DynamoDB excel at read-heavy workloads
- Built-in replication for read scaling

✅ **Easier to scale:**
- Horizontal scaling is simpler with NoSQL
- Add nodes as needed without complex sharding logic
- Automatic data distribution

**Why SQL (MySQL/PostgreSQL) Could Work:**

✅ **Strong consistency:**
- ACID transactions ensure no duplicate short URLs
- Strong consistency guarantees

✅ **Analytics queries:**
- Complex queries for analytics (if needed)
- SQL is better for aggregations and reporting

❌ **Scaling challenges:**
- Sharding SQL databases is more complex
- Managing billions of rows requires careful design
- More operational overhead

**Decision: Use NoSQL (DynamoDB, Cassandra, or Riak)**

**Specific Recommendations:**
- **DynamoDB (AWS):** Managed service, automatic scaling, pay-per-use
- **Cassandra:** Open-source, high availability, good for write-heavy too
- **Riak:** Simple key-value store, good for simple use cases

**Note:** If you need strong consistency guarantees or complex analytics, SQL is still viable, but requires more careful sharding design.

### 4.4 Data Partitioning (Sharding)

**Partition Key:** Short URL hash (`hash` field)

**NoSQL Partitioning:**
- **DynamoDB:** Automatic partitioning based on hash key
- **Cassandra:** Partition key = hash, distributes across nodes using consistent hashing
- **Riak:** Uses consistent hashing to distribute keys

**What is Consistent Hashing?**

**Consistent Hashing** is a distributed hashing technique that minimizes reorganization when nodes are added or removed from the system.

**Problem with Simple Hashing:**
```
Simple hash: hash(key) % num_partitions

Problem: If we add/remove a partition, most keys need to be moved!
- 10 partitions → 11 partitions: ~90% of keys need to move
- Very expensive rebalancing
```

**How Consistent Hashing Works:**

1. **Hash Ring:** Imagine a circle (ring) with values 0 to 2^64-1
2. **Hash Nodes:** Each partition/node is hashed and placed on the ring
3. **Hash Keys:** Each key is hashed and placed on the ring
4. **Assignment:** Key belongs to the first node clockwise from its position

**Example:**
```
Hash Ring (0 to 2^64-1):
    0
    |
    |  Node A (hash: 100)
    |  Node B (hash: 200)
    |  Node C (hash: 300)
    |
    Key "abc123" (hash: 150) → belongs to Node B (first node clockwise)
    Key "def456" (hash: 250) → belongs to Node C
    Key "ghi789" (hash: 50)  → belongs to Node A
```

**Benefits:**
- ✅ **Minimal Rebalancing:** When node added/removed, only nearby keys move
- ✅ **Even Distribution:** Keys distributed evenly across nodes
- ✅ **Scalability:** Easy to add/remove nodes

**Virtual Nodes (VNodes):**
- Each physical node has multiple virtual nodes on the ring
- Improves distribution and load balancing
- Example: 3 physical nodes × 100 virtual nodes = 300 positions on ring

**Partitioning Strategy:**
- Hash the short URL to determine partition using consistent hashing
- Example: `consistent_hash(hash)` → determines which node
- Ensures even distribution across partitions
- Minimal rebalancing when adding/removing nodes

**Number of Partitions:**
- Start with small number, scale as needed
- With 15TB data: 10-20 partitions (each ~1TB)
- DynamoDB/Cassandra handle partitioning automatically

**Replication:**
- **DynamoDB:** Automatic multi-AZ replication
- **Cassandra:** Replication factor (e.g., 3 replicas per partition)
- **Read scaling:** Read from any replica (eventual consistency OK for reads)

**What is Eventual Consistency?**

**Eventual Consistency** is a consistency model where the system will eventually become consistent, but there may be a temporary period where different replicas have different data.

**Consistency Models:**

1. **Strong Consistency:**
   - All replicas always have the same data
   - Read always returns latest write
   - Trade-off: Higher latency (must wait for all replicas)

2. **Eventual Consistency:**
   - Replicas will eventually have the same data
   - Read might return slightly stale data temporarily
   - Trade-off: Lower latency, but possible stale reads

**How Replication Works:**

```
Write Flow:
1. Client writes to primary/master node
2. Primary writes to local storage
3. Primary replicates to replicas (asynchronously)
4. Replicas update their data
5. Eventually all replicas have the same data

Read Flow:
1. Client reads from any replica
2. Replica returns its current data
3. If replication lag exists, might return slightly stale data
```

**Replication Lag:**
- Time between write to primary and replication to all replicas
- Typically: <100ms for same region, <500ms for cross-region
- During this time, replicas might have stale data

**Example:**
```
Time 0ms:  Write "abc123" → "https://example.com" to Primary
Time 10ms: Primary has data, Replica1 doesn't (replication in progress)
Time 50ms: Replica1 has data, Replica2 doesn't
Time 100ms: All replicas have data (eventually consistent)

If read happens at Time 30ms:
- Read from Primary: ✅ Returns latest data
- Read from Replica1: ✅ Returns latest data (already replicated)
- Read from Replica2: ⚠️ Returns stale data (not yet replicated)
```

**Why Eventual Consistency is OK for URL Shortener Reads:**

✅ **Read-Heavy Workload:**
- 100:1 read:write ratio
- Most requests are reads (redirects)
- Writes are rare (creating new URLs)

✅ **Low Latency Requirement (<100ms):**
- Strong consistency requires waiting for all replicas
- Eventual consistency allows reading from nearest replica
- Faster response time

✅ **Data Accuracy is Acceptable:**
- For URL redirects: Even if click_count is slightly stale, it's OK
- For URL lookup: Hash → URL mapping rarely changes (mostly immutable)
- Worst case: Read from replica that hasn't received latest write
  - If URL was just created, might not be in replica yet
  - But this is rare (writes are infrequent)
  - Can use read-after-write consistency for critical reads

✅ **Replication Lag is Small:**
- Same region: <10-50ms
- Cross-region: <100-200ms
- For URL redirects, this is acceptable

**Read-After-Write Consistency (Optional):**
- For critical reads (e.g., immediately after creating URL)
- Read from primary/master to ensure latest data
- Trade-off: Slightly higher latency

**For URL Shortener:**

**Write Pattern:**
- Write to primary partition
- Replicate to 3 replicas (in different AZs)
- Replication lag: <100ms

**Read Pattern:**
- Read from any replica (nearest for lowest latency)
- Eventual consistency OK because:
  - URL data is mostly immutable (hash → URL rarely changes)
  - Click counts can be slightly stale (acceptable)
  - Replication lag is small (<100ms)

**Latency <100ms Requirement:**
- ✅ **Achievable with eventual consistency:**
  - Read from nearest replica (low latency)
  - Don't wait for all replicas (strong consistency would add latency)
  - Replication lag <100ms means data is fresh enough

**Data Accuracy:**
- ✅ **Acceptable accuracy:**
  - URL redirects: Hash → URL mapping is accurate (rarely changes)
  - Analytics: Click counts might be slightly stale, but acceptable
  - User queries: Can use read-after-write for critical operations

**Summary:**
- **Partitions in AZs:** Data distributed across availability zones
- **Replicas:** Each partition has 3 replicas in different AZs
- **Consistent Hashing:** Distributes keys evenly, minimal rebalancing
- **Eventual Consistency:** OK for reads because:
  - Low latency (<100ms) - read from nearest replica
  - Data accuracy acceptable - URL data mostly immutable
  - Replication lag small (<100ms) - data is fresh enough

### 4.5 Indexing

**What is a Database Index?**

An **index** is a data structure that improves the speed of data retrieval operations on a database table. Think of it like an index in a book - instead of reading every page to find a topic, you look it up in the index.

**How Indexes Work:**
- Creates a separate data structure (usually B-tree or hash table)
- Stores sorted copies of indexed column values + pointers to actual rows
- Allows fast lookups without scanning entire table

**What is a B-Tree?**

A **B-tree** (Balanced Tree) is a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time.

**B-Tree Properties:**

1. **Balanced:** All leaf nodes are at the same depth
2. **Sorted:** Data is stored in sorted order (left to right)
3. **Multi-way:** Each node can have multiple children (not just 2 like binary tree)
4. **Order (m):** Maximum number of children a node can have
   - Typically: m = 100-1000 (depends on page size)
   - Example: Order 3 B-tree → max 3 children per node

**B-Tree Structure:**

```
                    [50, 100]          ← Root node (keys)
                   /    |    \
            [20,30]  [60,70]  [120,150]  ← Internal nodes
            /  |  \   /  |  \   /  |  \
          [10][25][40][55][65][80][110][130][200]  ← Leaf nodes
           │   │   │   │   │   │   │    │    │
           └───┴───┴───┴───┴───┴───┴────┴────┘
           Pointers to actual table rows
```

**How B-Tree Works:**

**1. Node Structure:**
- Each node contains:
  - Keys (sorted values from indexed column)
  - Pointers to child nodes (for internal nodes)
  - Pointers to actual table rows (for leaf nodes)

**2. Search Process:**
```
To find UserID = 123:

1. Start at root node
2. Compare 123 with keys in root:
   - If 123 < first key → go to left child
   - If 123 > last key → go to right child
   - Otherwise → go to middle child
3. Repeat at child node
4. Continue until reach leaf node
5. Leaf node contains pointer to actual row(s)
```

**Example Search:**
```
B-Tree Index on UserID:

Root:        [100, 500]
            /    |    \
      [50]  [200,300]  [700]
      / \    /  |  \    / \
   [10][75][150][250][400][800]

Search for UserID = 250:
1. Root: 250 is between 100 and 500 → go to middle child [200,300]
2. [200,300]: 250 is between 200 and 300 → go to middle child [250]
3. [250]: Found! → Get pointer to row(s) with UserID=250
4. Follow pointer to actual table row

Time: O(log n) - only 3 node accesses instead of scanning all rows!
```

**Why B-Tree Makes Lookups Faster:**

**1. Logarithmic Time Complexity:**
- **Without index:** O(n) - must check every row
- **With B-tree:** O(log n) - only traverse tree height
- **Example:** 1 billion rows
  - Without index: 1 billion comparisons
  - With B-tree: ~30 comparisons (log₂(1B) ≈ 30)

**2. Reduced Disk I/O:**
- B-tree nodes fit in disk pages (typically 4KB-16KB)
- Each node access = 1 disk read
- Example: 1 billion rows
  - Without index: 1 billion disk reads (worst case)
  - With B-tree: ~30 disk reads (tree height)

**3. Sequential Access:**
- Leaf nodes are linked (can traverse in order)
- Efficient for range queries (WHERE UserID BETWEEN 100 AND 200)
- Can scan leaf nodes sequentially

**4. Cache-Friendly:**
- Frequently accessed nodes stay in memory
- Root and upper levels cached → even faster

**How B-Tree Makes Joins Faster:**

**Join Example:**
```sql
SELECT u.*, url.*
FROM User u
JOIN URL url ON u.UserID = url.UserID
WHERE u.UserID = 123
```

**Without Indexes:**
```
1. Scan User table: Find UserID=123 → O(n) time
2. Scan URL table: Find all URLs with UserID=123 → O(n) time
Total: O(n²) - very slow!
```

**With B-Tree Indexes:**
```
1. Lookup User table index: Find UserID=123 → O(log n) time
2. Lookup URL table index: Find all URLs with UserID=123 → O(log n) time
3. Follow pointers to actual rows → O(1) per row
Total: O(log n) - much faster!
```

**Join Strategies Using B-Tree:**

**1. Index Nested Loop Join:**
```
For each row in User table:
  1. Use B-tree index on URL.UserID to find matching URLs
  2. O(log n) lookup per user
  3. Much faster than scanning entire URL table
```

**2. Merge Join (if both tables sorted):**
```
1. Both tables have B-tree indexes (sorted)
2. Traverse both indexes in parallel
3. Match rows with same UserID
4. O(n + m) time instead of O(n × m)
```

**B-Tree vs Other Data Structures:**

| Data Structure | Lookup Time | Range Queries | Disk I/O | Use Case |
|----------------|-------------|---------------|----------|----------|
| **B-Tree** | O(log n) | ✅ Excellent | Low | General-purpose indexes |
| **Hash Table** | O(1) | ❌ Poor | Low | Exact match only |
| **Binary Tree** | O(log n) | ✅ Good | High | In-memory only |

**What is "In-Memory" vs "Disk-Optimized"?**

**In-Memory:**
- Data structure stored entirely in RAM (Random Access Memory)
- Very fast access (nanoseconds)
- Limited by available RAM size
- Data is lost when program ends (unless persisted separately)
- Used for: Temporary data, caches, small datasets

**Disk-Optimized:**
- Data structure designed to work with disk storage
- Slower access (milliseconds - disk I/O is slow)
- Can handle very large datasets (terabytes)
- Data persists on disk
- Used for: Databases, file systems, large datasets

**Why Binary Tree is "In-Memory Only":**

**1. Node Structure:**
- Binary tree nodes are small (just key + 2 pointers)
- Each node access = potential disk read
- For 1 billion nodes: Tree height = ~30 levels
- Would require 30 disk reads per lookup (very slow!)

**2. Not Optimized for Disk Pages:**
- Disk reads happen in pages (4KB-16KB blocks)
- Binary tree nodes are small (~16-24 bytes)
- Reading one node = reading entire 4KB page (wasteful)
- Most of the page is unused

**3. Random Access Pattern:**
- Binary tree traversal jumps around randomly
- Disk is slow at random access
- Each jump = new disk read
- Very inefficient for disk storage

**4. Depth Problem:**
```
Binary Tree (in-memory):
- 1 billion nodes → ~30 levels deep
- In RAM: Fast (all nodes in memory)
- On disk: 30 disk reads per lookup = very slow!

B-Tree (disk-optimized):
- 1 billion nodes → ~3-4 levels deep (multi-way tree)
- Each node fits in disk page (4KB)
- Only 3-4 disk reads per lookup = much faster!
```

**Example Comparison:**

**Binary Tree (In-Memory):**
```
Structure:
        [50]
       /    \
    [25]    [75]
   /   \    /   \
 [10] [40][60] [90]

Access: All nodes in RAM → Very fast (nanoseconds)
Size: Limited by RAM (e.g., 16GB RAM = ~1 billion nodes max)
Persistence: Data lost when program ends
```

**B-Tree (Disk-Optimized):**
```
Structure:
              [50, 100]
             /    |    \
      [20,30]  [60,70]  [120,150]

Access: Nodes on disk → Slower (milliseconds per disk read)
Size: Limited by disk (e.g., 1TB disk = billions of nodes)
Persistence: Data persists on disk
```

**Why B-Tree is Better for Databases:**

✅ **Multi-way Tree:**
- Each node has many children (100-1000)
- Tree is much shallower (3-4 levels vs 30 levels)
- Fewer disk reads needed

✅ **Page-Sized Nodes:**
- Each node fits in one disk page (4KB)
- Reading one node = reading one page (efficient)
- No wasted space

✅ **Sequential Access:**
- Leaf nodes linked sequentially
- Can read multiple nodes in one disk operation
- Better for range queries

**Real-World Example:**

**Binary Tree (In-Memory):**
- Used in: Programming language data structures, in-memory caches
- Example: Python's `dict`, Java's `TreeMap` (when small)
- Size limit: ~1-10 million nodes (depends on RAM)
- Access time: ~100 nanoseconds

**B-Tree (Disk-Optimized):**
- Used in: Database indexes, file systems
- Example: MySQL indexes, PostgreSQL indexes, file system directories
- Size limit: Billions of nodes (limited by disk)
- Access time: ~1-10 milliseconds (disk I/O)

**For URL Shortener:**
- **Database indexes:** Use B-tree (disk-optimized, handles billions of rows)
- **In-memory cache:** Could use binary tree (fast, but limited size)
- **Redis cache:** Uses hash tables (even faster for exact lookups)
| **Sorted Array** | O(log n) | ✅ Excellent | High | Small datasets |

**Why B-Tree for Databases:**

✅ **Disk-Optimized:**
- Nodes sized to fit disk pages (4KB-16KB)
- Minimizes disk I/O
- Binary tree would be too deep (more disk reads)

✅ **Balanced:**
- Always maintains balance
- Guarantees O(log n) performance
- No worst-case O(n) scenarios

✅ **Range Queries:**
- Leaf nodes linked sequentially
- Efficient for BETWEEN, >, < queries
- Hash tables can't do this

✅ **Handles Large Data:**
- Works well with billions of rows
- Scales to disk storage
- Binary tree would be too deep

**B-Tree Example for URL Shortener:**

**Index on UserID:**
```
Root:           [5000000]
               /         \
      [2500000]          [7500000]
      /      \           /        \
[1250000] [3750000] [6250000] [8750000]
   ...       ...       ...       ...
```

**Query: SELECT * FROM URL WHERE UserID = 1234567**

1. Root: 1234567 < 5000000 → go left
2. [2500000]: 1234567 < 2500000 → go left
3. [1250000]: 1234567 > 1250000 → go right
4. Continue until leaf node
5. Found! → Get pointer to row(s)
6. Follow pointer to actual table row

**Time:** O(log n) = ~20-30 comparisons for 30 billion rows
**Without index:** O(n) = 30 billion comparisons

**Example:**
```
Without Index (Full Table Scan):
- Query: SELECT * FROM URL WHERE UserID = 123
- Database scans ALL 30 billion rows
- Time: O(n) - very slow!

With Index on UserID:
- Query: SELECT * FROM URL WHERE UserID = 123
- Database looks up UserID=123 in index (fast B-tree search)
- Gets pointer to matching rows
- Time: O(log n) - much faster!
```

**Why Use Indexes?**

✅ **Faster Reads:**
- **Without index:** Full table scan (check every row) - O(n) time
- **With index:** Index lookup (binary search) - O(log n) time
- **Speedup:** Can be 100x-1000x faster for large tables

✅ **Faster Joins:**
- Foreign key lookups are much faster with indexes
- Example: Joining URL and User tables

✅ **Faster Sorting:**
- ORDER BY queries are faster if column is indexed
- Index is already sorted

✅ **Faster Filtering:**
- WHERE clauses on indexed columns are much faster
- Example: `WHERE ExpirationDate < '2025-01-01'`

**Performance Impact:**

**Reads (SELECT queries):**
- ✅ **Much faster** with index
- Example: Finding all URLs by user
  - Without index: Scan 30 billion rows = seconds/minutes
  - With index: Lookup in index = milliseconds

**Writes (INSERT/UPDATE/DELETE):**
- ⚠️ **Slightly slower** with index
- Must update both table AND index
- Example: Inserting new URL
  - Without index: Insert 1 row
  - With index: Insert 1 row + update index = ~10-20% slower

**Space Usage:**

**Index Storage:**
- Indexes take additional disk space
- Typically 10-30% of table size (depends on column type and data)
- Example: 15TB URL table might need 1.5-4.5TB for indexes

**Index Size Calculation:**
```
Index on UserID (INT):
- UserID value: 4 bytes (INT)
- Row pointer: 4-8 bytes (depends on database)
- Overhead: ~10-20% (B-tree structure)
- Per index entry: ~10-15 bytes

For 30 billion URLs:
- Index size: 30B × 12 bytes = 360GB
- Plus overhead: ~400-450GB total
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

**What is Cardinality?**

**Cardinality** refers to the number of unique values in a column.

**Types of Cardinality:**

1. **High Cardinality:**
   - Many unique values
   - Example: `hash` (short URL) - billions of unique values
   - ✅ Good for indexing (index is very selective)

2. **Low Cardinality:**
   - Few unique values
   - Example: `status` column with values: "active", "inactive", "deleted" (only 3 values)
   - ❌ Poor for indexing (index not very selective)

3. **Medium Cardinality:**
   - Moderate number of unique values
   - Example: `user_id` - millions of unique values
   - ✅ Good for indexing

**Why Low Cardinality is Bad for Indexes:**

```
Example: Status column with 3 values (active, inactive, deleted)
- Table has 1 billion rows
- Index on status: Only 3 distinct values
- Query: WHERE status = 'active'
  - Index returns ~333 million rows (not very selective)
  - Might be faster to just scan the table
  - Index overhead not worth it
```

**Cardinality Examples:**

| Column | Unique Values | Cardinality | Good for Index? |
|--------|---------------|-------------|-----------------|
| `hash` (short URL) | 30 billion | Very High | ✅ Excellent |
| `user_id` | 10 million | High | ✅ Good |
| `country` | 195 countries | Medium | ⚠️ Maybe |
| `status` | 3 values | Low | ❌ No |
| `gender` | 2 values | Very Low | ❌ No |
| `created_month` | 12 months | Low | ❌ No |

**Rule of Thumb:**
- **High cardinality (>10% unique):** Good for indexing
- **Low cardinality (<1% unique):** Usually not worth indexing
- **Medium cardinality (1-10% unique):** Depends on query patterns

**Index Types:**

1. **Primary Index (Primary Key):**
   - Automatically created
   - Unique, not null
   - Fastest lookups

2. **Secondary Index:**
   - Created on non-primary key columns
   - Can be unique or non-unique
   - Example: `INDEX idx_user_id (UserID)`

3. **Composite Index:**
   - Index on multiple columns
   - Example: `INDEX idx_user_date (UserID, ExpirationDate)`
   - Useful for queries filtering on multiple columns

**Index Trade-offs:**

| Aspect | Without Index | With Index |
|--------|---------------|------------|
| **Read Speed** | Slow (full scan) | Fast (index lookup) |
| **Write Speed** | Fast | Slightly slower (must update index) |
| **Space** | Table only | Table + Index (10-30% more) |
| **Maintenance** | None | Index must be maintained |

**For URL Shortener:**

**Primary Key:**
- `hash` (partition key) - for lookups by short URL
- This is the main access pattern (99% of queries)
- Automatically indexed

**Secondary Indexes:**
- **`user_id` index:** For queries like "get all URLs by user"
  - Query: `SELECT * FROM URL WHERE UserID = 123`
  - Without index: Scan 30 billion rows (very slow!)
  - With index: Fast lookup (milliseconds)

- **`expires_at` index:** For cleanup jobs
  - Query: `SELECT * FROM URL WHERE ExpirationDate < NOW()`
  - Without index: Scan all rows (very slow!)
  - With index: Fast range query (milliseconds)

**NoSQL Indexing:**

**DynamoDB:**
- **Global Secondary Index (GSI):** On `user_id` for "get all URLs by user"
- **Local Secondary Index (LSI):** On sort key within partition
- Trade-off: GSIs consume additional read/write capacity

**Cassandra:**
- Secondary indexes are less efficient than in SQL
- Consider denormalization instead
- Example: Store user's URLs in separate table

**Expiration Cleanup:**
- Use TTL feature (if available) for automatic cleanup
- Or separate cleanup job with index on expiration date

**Note:** For NoSQL, minimize secondary indexes - they're less efficient than in SQL. Consider denormalizing data if you need frequent queries by user_id.

---

## Step 5: High-Level Design

### 5.1 System Architecture

```
[Client/Browser]
    ↓
[Load Balancer] (distributes requests)
    ↓
[Application Servers] (multiple instances)
    ↓
[Redis Cache] (hot URLs)
    ↓
[Database Shards] (with read replicas)
    ↓
[Analytics DB] (separate, write-heavy)
```

### 5.2 Core Components

1. **Load Balancer:**
   - Distributes incoming requests across application servers
   - Health checks to remove unhealthy servers
   - SSL termination

2. **Application Servers:**
   - Handle business logic
   - Generate short URLs
   - Handle redirects
   - Rate limiting
   - Multiple instances for scalability

3. **Redis Cache:**
   - Stores hot URLs (20% generating 80% traffic)
   - LRU eviction policy
   - Reduces database load

4. **Database (NoSQL):**
   - Stores URL mappings (key-value store)
   - DynamoDB/Cassandra/Riak for horizontal scaling
   - Automatic partitioning and replication
   - Optimized for billions of small records

5. **Analytics Database:**
   - Separate database for analytics (write-heavy)
   - Tracks clicks, referrers, geographic data
   - Use NoSQL (MongoDB/Cassandra) or time-series DB (InfluxDB) for flexibility

---

## Step 6: Detailed Design

### 6.1 Basic System Design and Algorithm

**The Core Problem:**
How to generate a short and unique key for a given URL?

Example: `http://tinyurl.com/jlg8zpc` - the last 6-7 characters (`jlg8zpc`) is the short key we want to generate.

**Approach 1: Encoding Actual URL (Hash-Based)**

**Concept:**
- Compute a unique hash (MD5, SHA256, etc.) of the given URL
- Encode the hash for display (Base36, Base62, or Base64)
- Use part of the encoded hash as the short key

**Encoding Options:**

1. **Base36:** `a-z` (26) + `0-9` (10) = 36 characters
2. **Base62:** `A-Z` (26) + `a-z` (26) + `0-9` (10) = 62 characters
3. **Base64:** `A-Z` (26) + `a-z` (26) + `0-9` (10) + `-` + `.` = 64 characters

**Key Length Calculation:**

| Length | Base62 | Base64 | Sufficient? |
|--------|--------|--------|-------------|
| 6 chars | 62^6 = ~56.8 billion | 64^6 = ~68.7 billion | ✅ Yes (for 30B URLs) |
| 7 chars | 62^7 = ~3.5 trillion | 64^7 = ~4.4 trillion | ✅ Yes (plenty) |
| 8 chars | 62^8 = ~218 trillion | 64^8 = ~281 trillion | ✅ Overkill |

**Hash Function Example (MD5):**
- MD5 produces 128-bit hash value
- **Base64 encoding:** Each character encodes **6 bits** (NOT 8 bits)
  - 64 possible characters = 2^6 = 6 bits per character
  - 128 bits ÷ 6 bits per character = ~21.3 characters (round to 21-22 characters)
- **Base62 encoding:** Each character encodes **~5.95 bits** (approximately 6 bits)
  - 62 possible characters ≈ 2^5.95
  - 128 bits ÷ 5.95 bits per character = ~21.5 characters (round to 21-22 characters)
- **Why not 8 bits?** 8 bits = 1 byte, but encoding uses fewer bits per character to represent more characters in the alphabet (64 or 62 characters vs 256 possible byte values)
- If we only need 6-8 characters, take first 6-8 characters from encoded string

**How Bits are Converted to Base64:**

**Base64 Encoding Process:**
1. **Input:** Binary data (128 bits from MD5 hash)
2. **Group bits:** Group into 6-bit chunks (since Base64 uses **6 bits per character**, NOT 8 bits)
   - Each 6-bit chunk represents one Base64 character
   - 128 bits ÷ 6 = 21.33 chunks → 21-22 characters
3. **Map to characters:** Each 6-bit value (0-63) maps to a Base64 character
4. **Output:** String of Base64 characters

**Example:**
```
MD5 Hash (128 bits):
10101101 11001100 11110000 10101010 ... (128 bits total)

Step 1: Group into 6-bit chunks
101011 | 011100 | 110011 | 110000 | 101010 | 10... (21 chunks)

Step 2: Convert each 6-bit chunk to decimal
101011 = 43
011100 = 28
110011 = 51
...

Step 3: Map to Base64 characters (A-Z, a-z, 0-9, +, /)
43 → 'r'
28 → 'c'
51 → 'z'
...

Result: "rcz..." (21 characters)
```

**Why Use MD5 if It's Not Secure?**

**Important Clarification:**
- ✅ **For URL Shortening:** We don't actually need MD5's security properties
- ✅ **We only need:** Uniqueness and distribution (not cryptographic security)
- ⚠️ **MD5 is insecure for:** Digital signatures, password hashing, security-critical applications
- ✅ **MD5 is OK for:** Non-security use cases like URL hashing, checksums, generating unique IDs

**Why MD5 Might Still Be Used (Non-Security Contexts):**

1. **Speed:**
   - MD5 is faster than SHA-256
   - For URL hashing (non-security), speed matters
   - SHA-256: ~200-300 MB/s
   - MD5: ~500-600 MB/s

2. **Fixed Output Size:**
   - MD5: Always 128 bits (16 bytes)
   - SHA-256: Always 256 bits (32 bytes)
   - For URL shortening, 128 bits is sufficient

3. **Legacy/Compatibility:**
   - Some systems already use MD5
   - Changing would break compatibility

4. **Non-Security Use Case:**
   - URL shortening doesn't need cryptographic security
   - We just need:
     - Uniqueness (low collision probability)
     - Distribution (even spread)
     - Speed (fast generation)

**Better Alternatives for URL Shortening:**

**Option 1: SHA-256 (More Secure, Still Fast)**
- ✅ More secure (not broken)
- ✅ Still fast enough
- ⚠️ Larger output (256 bits vs 128 bits)
- ✅ Recommended for new systems

**For URL Shortener - What the Book Recommends:**

**What the System Design Primer Book Recommends:**
The book focuses on **hash-based approaches**:
1. Hash URL + append user_id (if user signed in)
2. Hash URL + append sequence number (if no user tracking)

**Summary:**
- **Bits → Base64:** 6 bits per character (64 = 2^6), 128 bits = 128 ÷ 6 = ~21.3 characters (round to 21-22 characters)
- **Bits → Base62:** ~5.95 bits per character (62 ≈ 2^5.95), 128 bits = 128 ÷ 5.95 = ~21.5 characters (round to 21-22 characters)
- **Note:** Base64 uses 6 bits per character, NOT 8 bits. 8 bits = 1 byte, but Base64 encoding uses 6 bits per character to represent 64 possible values.
- **MD5 Security:** MD5 is insecure for security-critical uses, but OK for non-security uses like URL hashing
- **For URL Shortener (Following Book):** Use hash-based approach (SHA-256 + user_id or sequence)

**Algorithm:**
```
1. Take input URL: "https://example.com/very/long/url"
2. Hash it: MD5/SHA256 → 128-bit hash
3. Encode: Base62/Base64 → "aBc123XyZ456..."
4. Take first 6-8 characters: "aBc123"
5. Use as short key
```

**System Flow Diagram (Hash-Based Approach with Collision Handling):**

```
┌─────────┐
│ Client  │
└────┬────┘
     │ 1. Shorten a URL
     │
     ▼
┌─────────┐
│ Server  │
└────┬────┘
     │ 2. Encode URL
     │
     ▼
┌──────────┐
│ Encoding │
└────┬─────┘
     │ 3. Store encoded URL
     │
     ▼
┌──────────┐
│ Database │
└────┬─────┘
     │
     ├─── 4a. Successfully inserted ────┐
     │                                    │
     └─── 4b. Failed due to duplication ─┘
                                          │
                                          ▼
                                    ┌─────────┐
                                    │ Server  │
                                    └────┬────┘
                                         │ 5. Append sequence and encode
                                         │
                                         ▼
                                    ┌──────────┐
                                    │ Encoding │
                                    └────┬─────┘
                                         │ 6. Store encoded URL (retry)
                                         │
                                         ▼
                                    ┌──────────┐
                                    │ Database │
                                    └────┬─────┘
                                         │
                                         └─── 7. Successfully inserted
                                               │
                                               ▼
                                          ┌─────────┐
                                          │ Server  │
                                          └────┬────┘
                                               │ 8. Return shortened URL to Client
                                               │
                                               ▼
                                          ┌─────────┐
                                          │ Client  │
                                          └─────────┘
```

**Detailed Flow:**

1. **Client → Server:** Client sends "Shorten a URL" request
2. **Server → Encoding:** Server instructs Encoding component to "Encode URL"
3. **Encoding → Database:** Encoding component attempts to "Store encoded URL" in Database
4. **Database Response:**
   - **4a. Success Path:** Database reports "Successfully inserted" → Go to step 8
   - **4b. Collision Path:** Database reports "Failed due to duplication" → Go to step 5
5. **Server → Encoding:** Server instructs Encoding to "Append sequence and encode" (add sequence number to make unique)
6. **Encoding → Database:** Encoding attempts to "Store encoded URL" again with appended sequence
7. **Database:** Reports "Successfully inserted" (or repeats collision handling if still duplicate)
8. **Server → Client:** Server returns shortened URL to Client

**Key Points:**
- ✅ **Collision Detection:** Database checks if encoded URL already exists
- ✅ **Retry Mechanism:** If collision, append sequence number and retry
- ✅ **Automatic Handling:** System automatically handles collisions without user intervention
- ⚠️ **Performance Impact:** Multiple retries can slow down URL creation

**Problems with This Approach:**

❌ **Problem 1: Same URL = Same Short Key**
- If multiple users enter the same URL, they get the same shortened URL
- Not acceptable if we want unique short URLs per user
- Example:
  - User A: "https://example.com" → "abc123"
  - User B: "https://example.com" → "abc123" (same!)

❌ **Problem 2: URL Encoding Issues**
- URLs can be encoded differently but represent the same resource
- Example:
  - `http://www.educative.io/distributed.php?id=design`
  - `http://www.educative.io/distributed.php%3Fid%3Ddesign` (URL-encoded)
- These are identical but hash to different values
- Results in duplicate short URLs for the same resource

**Workarounds:**

**Solution 1: Append Sequence Number**
```
1. Append increasing sequence number to URL
2. Hash the combined string
3. Generate short key

Example:
- URL: "https://example.com"
- Sequence: 1 → Hash("https://example.com1") → "abc123"
- Sequence: 2 → Hash("https://example.com2") → "def456"
```

**Issues:**
- ⚠️ Ever-increasing sequence number (can overflow)
- ⚠️ Performance impact (must track sequence)
- ⚠️ Don't need to store sequence in database

**Solution 2: Append User ID**
```
1. Append user_id to URL (if user is signed in)
2. Hash the combined string
3. Generate short key

Example:
- URL: "https://example.com"
- User ID: "user_12345"
- Hash("https://example.comuser_12345") → "xyz789"
```

**How This Solves Duplication:**

✅ **Yes, this solves the duplication problem!**

**Why it works:**
- Different users → Different user_ids → Different hash inputs → Different short keys
- Same URL + Different user = Different short key
- Same URL + Same user = Same short key (which is OK - user gets their own short URL)

**Example:**
```
User A (user_id: "user_12345"):
- URL: "https://example.com"
- Input: "https://example.com" + "user_12345" = "https://example.comuser_12345"
- Hash → "abc123"
- Result: User A gets "abc123"

User B (user_id: "user_67890"):
- URL: "https://example.com" (same URL!)
- Input: "https://example.com" + "user_67890" = "https://example.comuser_67890"
- Hash → "def456" (different hash!)
- Result: User B gets "def456" (different short key!)

✅ No duplication! Each user gets unique short URL even for same original URL
```

**Issues:**
- ⚠️ **If user not signed in:** Must ask user to choose uniqueness key or use session ID
- ⚠️ **If conflict still occurs:** Must keep generating until unique (very rare with user_id)
- ✅ **Better than sequence number:** No overflow risk, no global counter needed
- ✅ **Per-user uniqueness:** Each user can have their own short URL for same original URL

**Handling Anonymous Users:**

**Option 1: Session ID**
```
If user not signed in:
- Use session ID (temporary identifier)
- Hash(URL + session_id) → unique short key
- Session expires → short URL still works (stored in database)
```

**Option 2: Ask User for Custom Alias**
```
If user not signed in:
- Ask user to provide custom alias
- If alias available → use it
- If alias taken → ask for different one
```

**Option 3: Generate Random ID**
```
If user not signed in:
- Generate random UUID or random string
- Hash(URL + random_id) → unique short key
- Store random_id with URL (for future reference if needed)
```

**Collision Handling:**

Even with user_id, collisions are possible (very rare):
- Two different URLs + two different users might hash to same short key
- Probability: Extremely low (1 in billions)
- Solution: Check database, if collision → append sequence number and retry

**Complete Algorithm with User ID:**
```
1. Get original URL and user_id (if signed in)
2. If user_id exists:
   - Combine: original_url + user_id
   - Hash: SHA256(original_url + user_id)
   - Encode: Base62(hash)
   - Take first 7 characters: short_key
3. If user_id doesn't exist:
   - Use session_id or ask for custom alias
   - Combine: original_url + session_id/custom_alias
   - Hash and encode as above
4. Check database for collision
5. If collision:
   - Append sequence number: original_url + user_id + sequence
   - Re-hash and retry
6. Store: short_key → original_url mapping
7. Return short_key to user
```

**For URL Shortener - Comparison of Approaches (As Per Book):**

**What the Book Recommends:**
The System Design Primer book focuses on **hash-based approaches** with workarounds:
1. Hash URL + append sequence number (if collision)
2. Hash URL + append user_id (if user signed in)

**Comparison:**

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| **Hash + Sequence** | ✅ No overflow (if handled) | ⚠️ Performance impact<br>⚠️ Ever-increasing counter<br>⚠️ Collision handling needed | Book's approach for anonymous users |
| **Hash + User ID** | ✅ No overflow<br>✅ Per-user uniqueness<br>✅ No global counter | ⚠️ Requires user sign-in<br>⚠️ Collision handling needed<br>⚠️ Anonymous users need workaround | Per-user unique URLs (book's approach) |

**Recommended for URL Shortener (Following Book's Approach):**

**Option 1: Hash URL + User ID (If per-user uniqueness needed)**
```
1. Combine: original_url + user_id (if signed in)
2. Hash: SHA256(original_url + user_id)
3. Encode: Base62
4. Take first 7 characters
5. Check for collision (very rare)
6. If collision, append sequence number and retry
```

**Option 2: Hash URL + Sequence (If no user tracking)**
```
1. Get next sequence number
2. Combine: original_url + sequence_number
3. Hash: SHA256(original_url + sequence_number)
4. Encode: Base62
5. Take first 7 characters
6. Check for collision (very rare)
7. If collision, increment sequence and retry
```

**Why Hash-Based (Book's Approach) is Good:**
- ✅ Works with distributed systems (no single counter)
- ✅ No single point of failure
- ✅ Scales horizontally
- ✅ Handles anonymous users (with session ID or custom alias)
- ✅ Per-user uniqueness (if using user_id)

**Our Recommendation (Following Book):**
- Use **Hash + User ID** approach (if users can sign in)
- Use **Hash + Sequence** approach (if no user tracking)
- This is what interviewers expect
- This is what the book teaches
- Works well for distributed systems

**Implementation (Hash + User ID - Following Book's Approach):**
```python
# Pseudo-code - Hash-based approach (as per System Design Primer book)
def generate_short_url(original_url, user_id=None):
    sequence = 0
    max_retries = 10

    while sequence < max_retries:
        # Combine URL with user_id or session/sequence
        if user_id:
            # Book's approach: Append user_id to make unique
            input_string = original_url + user_id
        else:
            # For anonymous users: Use session_id or ask for custom alias
            session_id = get_session_id() or generate_random_id()
            input_string = original_url + session_id

        # Append sequence if retry (collision handling)
        if sequence > 0:
            input_string = input_string + str(sequence)

        # Hash the combined string (SHA256 as recommended)
        hash_value = sha256(input_string)

        # Encode to Base62
        encoded = base62_encode(hash_value)

        # Take first 7 characters
        short_key = encoded[:7]

        # Check for collision (as per book)
        if not db.exists(short_key):
            # Store mapping
            db.store(short_key, original_url, user_id)
            return short_key

        # Collision detected, retry with incremented sequence
        sequence += 1

    # If max retries reached, use longer key or different approach
    raise Exception("Unable to generate unique short URL")
```

**Approach 2: Generating Keys Offline (Key Generation Service - KGS)**

**Concept:**
- Have a standalone **Key Generation Service (KGS)** - a separate server/service that generates random keys beforehand
- KGS uses **two tables** in its database (key-DB):
  1. **Unused Keys Table:** Keys not yet assigned to any URL
  2. **Used Keys Table:** Keys already assigned to URLs
- Store pre-generated keys in the unused keys table
- When shortening a URL, app servers request a key from KGS
- KGS provides a key from unused table and moves it to used table
- No encoding needed, no collisions, no duplicates

**How It Works:**

```
1. KGS pre-generates random 6-7 character keys (Base62/Base64)
2. Stores keys in key-DB (database of unused keys)
3. When app server needs a key:
   - Request key from KGS
   - KGS provides unused key from key-DB
   - KGS marks key as used
4. App server uses key for URL shortening
```

**Benefits:**
- ✅ **Simple and fast:** No encoding, no hashing needed
- ✅ **No collisions:** Keys are pre-generated and guaranteed unique
- ✅ **No duplicates:** KGS ensures all keys are unique
- ✅ **Fast assignment:** Just grab a key from pool

**Key-DB Size Calculation:**

**Important Distinction:**
- **Encoding bits:** Base64 uses 6 bits of information per character, Base62 uses ~5.95 bits per character
- **Storage bytes:** When stored as a string in database/file, each character takes **1 byte** (ASCII characters)
- **Why 1 byte?** Each Base64/Base62 character (like 'A', 'B', '1', 'a') is an ASCII character, which requires 1 byte to store

**With Base64 encoding (6 characters):**
- 64^6 = ~68.7 billion unique keys
- **Storage:** 6 characters × **1 byte per character** = 6 bytes per key
  - Each character (e.g., 'A', 'B', '1', '+') is stored as 1 byte in ASCII
  - Even though each character encodes 6 bits of information, it still takes 1 byte to store the character itself
- Total size: 6 bytes × 68.7B = **412 GB**

**With Base62 encoding (6 characters):**
- 62^6 = ~56.8 billion unique keys
- **Storage:** 6 characters × **1 byte per character** = 6 bytes per key
- Total size: 6 bytes × 56.8B = **341 GB**

**With Base62 encoding (7 characters):**
- 62^7 = ~3.5 trillion unique keys
- **Storage:** 7 characters × **1 byte per character** = 7 bytes per key
- Total size: 7 bytes × 3.5T = **24.5 TB** (too large!)

**Why 1 Byte Per Character (Not 6/8 = 0.75 Bytes)?**

**Encoding vs Storage:**
- **Encoding (Base64):** Each character represents 6 bits of information
- **Storage (ASCII):** Each character is stored as 1 byte (8 bits) in memory/disk

**Example:**
```
Key: "aBc123" (6 characters)
- Information: 6 chars × 6 bits = 36 bits of information
- Storage: 6 chars × 1 byte = 6 bytes in database/file
- Why? Each character ('a', 'B', 'c', '1', '2', '3') is an ASCII character
- ASCII characters are stored as 1 byte each (even if they encode less than 8 bits of information)
```

**Could We Store More Efficiently?**
- **Theoretical minimum:** 36 bits ÷ 8 = 4.5 bytes (but we can't store half bytes)
- **Practical:** We store as string (6 bytes) because:
  - Easier to work with (string operations, indexing, etc.)
  - Database VARCHAR/TEXT stores characters, not raw bits
  - The overhead is acceptable (6 bytes vs 5 bytes minimum)

**Recommendation:**
- Use 6 characters with Base64: 412 GB (manageable)
- Or use 6 characters with Base62: 62^6 = ~56.8B keys = 6 bytes × 56.8B = **341 GB**

**Multiple App Servers - Brief Explanation:**

**What are Multiple App Servers?**

In a distributed system, we don't run our URL shortening service on a single server. Instead, we use **multiple app servers** (also called application servers or web servers) to handle requests.

**Why Multiple Servers?**
- ✅ **Handle high traffic:** 20K redirects/second requires multiple servers
- ✅ **Fault tolerance:** If one server dies, others continue serving
- ✅ **Horizontal scaling:** Add more servers as traffic grows
- ✅ **Load distribution:** Spread requests across servers

**Architecture:**
```
                    ┌─────────────┐
                    │ Load Balancer│
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌────▼────┐       ┌────▼────┐
   │ App     │       │ App     │       │ App     │
   │ Server 1│       │ Server 2│       │ Server 3│
   └────┬────┘       └────┬────┘       └────┬────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    ┌──────▼───────┐
                    │   Database   │
                    │   (Shared)   │
                    └──────────────┘
```

**How It Works:**
1. **Load Balancer:** Receives all requests, distributes to app servers
2. **App Servers:** Each server can handle URL shortening and redirects
3. **Shared Database:** All servers read/write to the same database (for URL mappings)
4. **KGS (Separate Server):** All app servers request keys from the same KGS service
   - KGS is a separate server/service (not an app server)
   - KGS uses its own database with 2 tables (unused keys, used keys)
   - App servers don't access KGS tables directly - they request keys via API

**Example:**
- 3 app servers, each can handle ~7K requests/second
- Total capacity: 3 × 7K = 21K requests/second
- If one server dies, remaining 2 servers handle 14K requests/second

**Concurrency Problem:**

**Problem:**
- Multiple servers reading keys concurrently from KGS
- Two servers might try to read the same key at the same time
- Same key assigned to multiple URLs → collision!

**Solution: Two-Table Approach**

**KGS is a separate server/service that uses two tables in its database:**

1. **Unused Keys Table (key-DB):** Keys not yet assigned to any URL
   - Pre-generated keys waiting to be used
   - KGS loads keys from here into memory

2. **Used Keys Table:** Keys already assigned to URLs
   - Keys that have been given to app servers
   - Prevents keys from being reused

**Process Overview:**
```
1. KGS loads batch of keys from unused table into memory
2. KGS moves those keys to used table (atomically)
3. KGS serves keys from memory to app servers
4. Each server gets unique keys (no conflicts)
```

**Detailed Lock Sequence:**

**Step 1: Loading Keys from Database to Memory (KGS Operation)**

```
1. Lock unused_keys table
   └─> Prevents other KGS instances from reading same keys

2. Read batch of keys from unused_keys table
   └─> Get 1000 keys (example)

3. Move keys to used_keys table (atomic operation)
   └─> Still holding unused_keys lock
   └─> Ensures keys are marked as used before anyone else can access them

4. Unlock unused_keys table
   └─> Release database lock

5. Lock memory_cache
   └─> Prevents app servers from accessing cache while updating

6. Add keys to memory_cache
   └─> Store keys in KGS server's memory

7. Unlock memory_cache
   └─> Release memory cache lock
   └─> Keys are now available for app servers
```

**Step 2: Assigning Key(s) to App Server (When Server Requests Key)**

**Scenario A: App Server Requests Single Key (No Caching)**

```
1. App server requests one key from KGS
2. KGS: Lock memory_cache
   └─> Prevents other app servers from getting same key
3. KGS: Remove one key from memory_cache
   └─> Get key (e.g., "aBc123")
4. KGS: Unlock memory_cache
   └─> Release lock immediately after removing key
5. KGS: Return key to app server
   └─> Key is now assigned to that server
   └─> No need to update used_keys table (already done in Step 1)
```

**Scenario B: App Server Requests Batch of Keys (For Local Caching)**

```
1. App server requests batch of keys from KGS (e.g., 100 keys)
2. KGS: Lock memory_cache
   └─> Prevents other app servers from getting same keys
3. KGS: Remove batch of keys from memory_cache
   └─> Get 100 keys (e.g., ["aBc123", "dEf456", ...])
4. KGS: Unlock memory_cache
   └─> Release lock immediately after removing keys
5. KGS: Return batch of keys to app server
6. App server: Store keys in local memory cache
   └─> Keys are now cached locally on app server
   └─> App server can use these keys without requesting from KGS
7. When app server needs a key:
   └─> Use key from local cache (no KGS call needed)
   └─> When local cache empty, request new batch from KGS
```

**Important:** In both scenarios, the `used_keys` table was already updated in Step 1 (when KGS loaded keys from database to memory). The app server caching is just for performance - keys are already marked as used in the database.

**Complete Flow Examples:**

**Example 1: Single Key Request (No App Server Caching)**

```
Time | Operation                    | Lock Status
-----|------------------------------|----------------------------------
T1   | App Server 1 requests 1 key | No locks
T2   | KGS: Lock memory_cache       | memory_cache: LOCKED
T3   | KGS: Check cache (empty)     | memory_cache: LOCKED
T4   | KGS: Unlock memory_cache     | No locks
T5   | KGS: Lock unused_keys table  | unused_keys: LOCKED
T6   | KGS: Read 1000 keys           | unused_keys: LOCKED
T7   | KGS: Move to used_keys table  | unused_keys: LOCKED, used_keys: LOCKED
T8   | KGS: Unlock unused_keys      | used_keys: LOCKED
T9   | KGS: Unlock used_keys        | No locks
T10  | KGS: Lock memory_cache       | memory_cache: LOCKED
T11  | KGS: Add 1000 keys to cache  | memory_cache: LOCKED
T12  | KGS: Unlock memory_cache     | No locks
T13  | KGS: Lock memory_cache       | memory_cache: LOCKED
T14  | KGS: Remove key "aBc123"     | memory_cache: LOCKED
T15  | KGS: Unlock memory_cache     | No locks
T16  | KGS: Return "aBc123" to App  | No locks
     | Server 1                      |
T17  | App Server 1: Use key        | No locks (local operation)
```

**Example 2: Batch Key Request (With App Server Caching)**

```
Time | Operation                          | Lock Status
-----|------------------------------------|----------------------------------
T1   | App Server 1 requests 100 keys     | No locks
T2   | KGS: Lock memory_cache             | memory_cache: LOCKED
T3   | KGS: Check cache (has keys)         | memory_cache: LOCKED
T4   | KGS: Remove 100 keys from cache    | memory_cache: LOCKED
T5   | KGS: Unlock memory_cache            | No locks
T6   | KGS: Return 100 keys to App Server  | No locks
T7   | App Server 1: Store in local cache  | No locks (local to app server)
T8   | App Server 1: Use key from cache   | No locks (local operation)
     | (no KGS call needed)                |
T9   | App Server 1: Use another key       | No locks (local operation)
     | (no KGS call needed)                |
...  | (continues using cached keys)       | No locks
T100 | App Server 1: Cache empty          | No locks
T101 | App Server 1: Request new batch    | No locks
     | (repeat from T1)                     |
```

**Important Points:**

1. **Two Separate Operations:**
   - **Loading keys:** Database → Memory (happens when cache is empty)
   - **Assigning keys:** Memory → App Server (happens on each request)

2. **Lock Granularity:**
   - **Database locks:** Protect unused_keys and used_keys tables
   - **Memory cache lock:** Protects in-memory key pool

3. **Why Move to Used Table Before Memory?**
   - Ensures keys are marked as "used" in database immediately
   - If KGS dies after loading to memory, keys are already marked as used
   - Prevents key loss/duplication

4. **Why Lock Memory Cache?**
   - Multiple app servers can request keys simultaneously
   - Lock ensures only one server gets a specific key
   - Prevents race conditions

**Simplified Sequence (Correct Order):**

**Loading Keys (KGS Operation):**
```
1. Lock unused_keys
2. Get keys from unused_keys
3. Move keys to used_keys (atomic)
4. Unlock unused_keys
5. Lock memory_cache
6. Add keys to memory_cache
7. Unlock memory_cache
```

**Assigning Key (App Server Request):**
```
1. Lock memory_cache
2. Remove one key from memory_cache
3. Unlock memory_cache
4. Return key to app server
```

**Note:** The used_keys table is updated during Step 1 (loading), not during Step 2 (assigning). Once keys are in memory_cache, they're already marked as used in the database.

**Synchronization and Locking:**

**The Problem:**
- KGS must ensure it doesn't give the same key to multiple servers
- Without proper locking, two servers could request keys simultaneously
- Both servers might get the same key → collision!

**The Solution: Locking the Data Structure**

KGS must **synchronize (or get a lock on) the data structure holding the keys** before:
- Removing keys from the unused table
- Moving keys to the used table
- Assigning keys to servers

**How Locking Works:**

**1. Lock on Unused Keys Table:**
```
When KGS needs to load keys:
1. Acquire lock on unused_keys table
2. Read batch of keys (e.g., 1000 keys)
3. Move keys to used_keys table (atomically)
4. Release lock
5. Store keys in memory cache
```

**2. Lock on Memory Cache:**
```
When app server requests a key:
1. Acquire lock on memory cache (in-memory data structure)
2. Remove one key from cache
3. Release lock
4. Return key to app server
```

**Why Both Locks Are Needed:**

**Database Lock (Unused Keys Table):**
- Prevents multiple KGS instances from loading the same keys
- Ensures atomic move from unused → used table
- Critical when KGS has standby replica

**Memory Cache Lock:**
- Prevents multiple app servers from getting the same key from memory
- Ensures thread-safe access to in-memory key pool
- Critical for concurrent key assignment

**Implementation Example:**

```python
# Pseudo-code for KGS with proper locking
import threading

class KeyGenerationService:
    def __init__(self):
        self.unused_keys_table = "unused_keys"
        self.used_keys_table = "used_keys"
        self.memory_cache = []  # In-memory key pool
        self.cache_lock = threading.Lock()  # Lock for memory cache
        self.db_lock = threading.Lock()  # Lock for database operations
        self.cache_size = 1000

    def load_keys_to_memory(self):
        """Load batch of keys from unused table to memory"""
        # Step 1: Acquire database lock
        with self.db_lock:
            # Step 2: Read keys from unused table
            keys = db.get_batch(self.unused_keys_table, self.cache_size)

            # Step 3: Move keys to used table (atomic operation)
            db.move_to_table(keys, self.used_keys_table)

        # Step 4: Acquire memory cache lock
        with self.cache_lock:
            # Step 5: Add keys to memory cache
            self.memory_cache.extend(keys)

        # Locks are automatically released when 'with' block exits

    def get_key(self):
        """Provide key to app server (thread-safe)"""
        # Check if cache is empty
        if not self.memory_cache:
            self.load_keys_to_memory()  # Reload if empty

        # Acquire lock on memory cache
        with self.cache_lock:
            # Remove one key from cache
            if self.memory_cache:
                key = self.memory_cache.pop(0)
                return key
            else:
                # Cache empty, reload
                self.load_keys_to_memory()
                key = self.memory_cache.pop(0)
                return key
```

**Lock Types:**

**1. Database-Level Lock:**
- **Row-level lock:** Lock specific rows in unused_keys table
- **Table-level lock:** Lock entire table (simpler, but less concurrent)
- **Transaction lock:** Use database transactions to ensure atomicity

**2. Application-Level Lock:**
- **Mutex (Mutual Exclusion):** Single-threaded access to memory cache
- **Semaphore:** Limit concurrent access (e.g., max 10 concurrent key requests)
- **Read-Write Lock:** Multiple readers, single writer

**3. Distributed Lock (If KGS is Distributed):**
- **Redis Distributed Lock:** Use Redis for locking across multiple KGS instances
- **ZooKeeper Lock:** Use ZooKeeper for distributed coordination
- **Database Lock:** Use database row-level locking for distributed systems

**Example Scenario Without Locking (Race Condition):**

```
Time  | Server 1              | Server 2              | KGS Memory Cache
------|----------------------|----------------------|------------------
T1    | Request key          |                       | [key1, key2, key3]
T2    |                       | Request key           | [key1, key2, key3]
T3    | Read key1 (no lock)  | Read key1 (no lock)   | [key2, key3]
T4    | Return key1          | Return key1           | [key2, key3]
      | ❌ COLLISION! Both servers got key1
```

**Example Scenario With Locking (Correct):**

```
Time  | Server 1              | Server 2              | KGS Memory Cache
------|----------------------|----------------------|------------------
T1    | Request key          |                       | [key1, key2, key3]
T2    | Acquire lock         |                       | [key1, key2, key3] (locked)
T3    | Read key1            | Request key (wait)     | [key2, key3] (locked)
T4    | Release lock         | Acquire lock          | [key2, key3]
T5    | Return key1          | Read key2             | [key3]
T6    |                      | Release lock          | [key3]
T7    |                      | Return key2           | [key3]
      | ✅ No collision! Each server got unique key
```

**Key Points:**
- ✅ **Lock before access:** Always acquire lock before reading/modifying keys
- ✅ **Atomic operations:** Move keys from unused → used atomically
- ✅ **Release promptly:** Release lock as soon as operation completes
- ✅ **Prevent deadlocks:** Use consistent lock ordering
- ✅ **Handle failures:** If KGS dies while holding lock, use lock timeout/expiration

**Key Management Strategy:**

**Option 1: Move to Used Table When Loaded (Simpler)**
```
1. KGS loads 1000 keys from unused table
2. Immediately moves all 1000 to used table
3. Serves keys from memory to app servers
4. If KGS dies, some keys wasted (acceptable - we have billions)
```

**Option 2: Move to Used Table When Assigned (More Efficient)**
```
1. KGS loads 1000 keys into memory (stays in unused table)
2. When server requests key, assign from memory
3. Move assigned key to used table
4. More efficient (no wasted keys), but more complex
```

**Single Point of Failure:**

**Problem:**
- KGS is a single point of failure
- If KGS dies, no new keys can be generated

**Solution: Standby Replica**
- Have a **standby replica** of KGS
- When primary KGS dies, standby takes over
- Standby can continue generating and providing keys
- Ensures high availability

**App Server Caching:**

**Can app servers cache keys?**

✅ **Yes, this speeds things up!**

**How it works:**
```
1. App server requests batch of keys from KGS (e.g., 1000 keys)
2. KGS provides keys and marks them as used
3. App server caches keys in memory
4. When shortening URL, use cached key (no KGS call needed)
5. When cache empty, request new batch from KGS
```

**Benefits:**
- ✅ **Faster:** No KGS call for each URL (use cached key)
- ✅ **Reduced load:** Fewer requests to KGS
- ✅ **Lower latency:** Key available immediately

**Trade-off:**
- ⚠️ **Key loss:** If app server dies before using all cached keys, those keys are wasted
- ✅ **Acceptable:** We have 68.7B keys, losing a few thousand is fine

**Key Lookup Process:**

**When user accesses short URL:**

```
1. User clicks: http://tinyurl.com/abc123
2. App server extracts key: "abc123"
3. Lookup in database/key-value store:
   - Key exists → Get original_url
   - Key doesn't exist → Not found
4. Response:
   - If found: HTTP 302 Redirect with Location: original_url
   - If not found: HTTP 404 Not Found (or redirect to homepage)
```

**HTTP 302 Redirect:**
- **302 Found (Temporary Redirect):** Standard for URL shorteners
- Response header: `Location: https://original-url.com`
- Browser automatically follows redirect

**Custom Alias Size Limits:**

**Should we impose size limits on custom aliases?**

✅ **Yes, it's reasonable and desirable**

**Reasons:**
- Ensures consistent URL database
- Prevents abuse (very long custom aliases)
- Easier to manage and validate

**Size Limit:**
- **Maximum 16 characters per custom alias** (as per database schema)
- Example: `tinyurl.com/my-custom-link` (16 chars max)

**Validation:**
- Check custom alias length (≤ 16 characters)
- Check if custom alias already exists
- If exists → Return 409 Conflict
- If valid → Use custom alias as short key

**KGS Architecture:**

```
┌─────────────┐
│   KGS       │
│  (Primary)  │
└──────┬──────┘
       │
       ├─── Unused Keys Table (key-DB)
       │    - Pre-generated keys
       │    - Available for assignment
       │
       ├─── Used Keys Table
       │    - Assigned keys
       │    - Tracked to prevent reuse
       │
       └─── Memory Cache
            - Batch of keys loaded
            - Fast assignment to servers

┌─────────────┐
│   KGS       │
│  (Standby)  │  ← Takes over if primary dies
└─────────────┘
```

**KGS Implementation:**

```python
# Pseudo-code for KGS
class KeyGenerationService:
    def __init__(self):
        self.unused_keys_table = "unused_keys"
        self.used_keys_table = "used_keys"
        self.memory_cache = []  # Batch of keys in memory
        self.cache_size = 1000

    def load_keys_to_memory(self):
        """Load batch of keys from unused table to memory"""
        # Acquire database lock before accessing unused_keys table
        with self.db_lock:  # Synchronize database access
            keys = db.get_batch(self.unused_keys_table, self.cache_size)
            db.move_to_table(keys, self.used_keys_table)  # Mark as used (atomic)

        # Acquire memory cache lock before modifying cache
        with self.cache_lock:  # Synchronize memory cache access
            self.memory_cache.extend(keys)

    def get_key(self):
        """Provide key to app server (thread-safe)"""
        if not self.memory_cache:
            self.load_keys_to_memory()  # Reload if empty

        # Acquire lock on memory cache before removing key
        with self.cache_lock:  # Synchronize access to prevent duplicate keys
            if self.memory_cache:
                key = self.memory_cache.pop(0)  # Get from cache
                return key
            else:
                # Cache empty, reload
                self.load_keys_to_memory()
                key = self.memory_cache.pop(0)
                return key

    def pre_generate_keys(self, count):
        """Pre-generate random keys"""
        keys = []
        for i in range(count):
            key = generate_random_key(6)  # 6-char Base64
            keys.append(key)
        db.insert_batch(self.unused_keys_table, keys)
```

**App Server Implementation:**

```python
# Pseudo-code for App Server
class URLShortener:
    def __init__(self):
        self.kgs = KeyGenerationService()
        self.key_cache = []  # Cache keys locally
        self.cache_size = 100

    def get_key_from_kgs(self):
        """Request batch of keys from KGS"""
        keys = self.kgs.get_batch(self.cache_size)
        self.key_cache.extend(keys)

    def shorten_url(self, original_url):
        """Shorten URL using pre-generated key"""
        if not self.key_cache:
            self.get_key_from_kgs()  # Request more keys

        key = self.key_cache.pop(0)  # Use cached key
        db.store(key, original_url)
        return key
```

**Comparison: Approach 1 vs Approach 2**

| Aspect | Approach 1 (Hash-based) | Approach 2 (KGS) |
|--------|------------------------|------------------|
| **Key Generation** | On-demand (hash URL) | Pre-generated (offline) |
| **Speed** | Slower (hashing + encoding) | Faster (just grab key) |
| **Collisions** | Possible (need handling) | None (pre-validated) |
| **Complexity** | Medium (hash + collision handling) | Higher (KGS service) |
| **Storage** | No key storage needed | 412 GB for key-DB |
| **Single Point of Failure** | No (distributed) | Yes (KGS, but has standby) |
| **Scalability** | Good (no central service) | Good (KGS can scale) |

**For URL Shortener:**

**Both approaches are valid:**
- **Approach 1 (Hash-based):** Simpler, no key storage, works distributed
- **Approach 2 (KGS):** Faster, no collisions, but requires key storage and KGS service

**Recommendation:**
- **For interviews:** Know both approaches
- **Approach 1** is simpler and more commonly discussed
- **Approach 2** is faster but adds complexity (KGS service)

**Base62 Encoding:**
- Characters: `a-z` (26) + `A-Z` (26) + `0-9` (10) = 62 characters
- Example: `0-9a-zA-Z` = `0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`

**Hash Length: 7 characters**
- 62^7 = 3,521,614,606,208 unique combinations
- More than enough for 30 billion URLs
- Can handle: 3.5 trillion URLs (100x our requirement)

**Collision Handling (if using hash-based approach):**
- Probability of collision is extremely low
- If collision detected, append random character or use longer hash
- Can also use 8 characters if needed (62^8 = 218 trillion)

### 6.2 Caching Strategy (Moved to Step 8)

**Note:** The detailed caching strategy has been moved to **Step 8: Cache** to match the book's structure. This section is kept here for reference but the full content is in Step 8.

**Why Caching is Needed:**

We can cache URLs that are frequently accessed to improve performance. Instead of hitting the backend database for every redirect request, we can quickly check if the cache has the desired URL.

**Benefits:**
- ✅ **Faster response times:** Cache lookups are much faster than database queries (<1ms vs 10-50ms)
- ✅ **Reduced database load:** Cache handles hot URLs, database handles cache misses
- ✅ **Better scalability:** Cache can handle much higher read throughput than database
- ✅ **Cost effective:** Memory is cheaper than database compute for read-heavy workloads

**What to Cache:**

- **Hot URLs:** URLs that are frequently accessed (20% generating 80% traffic)
- **Cache key:** `short_url:{hash}` (e.g., `short_url:aBc123`)
- **Cache value:** `original_url` (e.g., `https://example.com/very/long/url`)
- **Full URL mapping:** Store both short key and original URL for quick lookup

**Cache Solution:**

**Off-the-Shelf Solutions:**
- **Memcached:** Simple, fast, distributed memory caching
- **Redis:** More features (persistence, data structures, pub/sub)
- **Both are suitable:** For URL shortener, either works well

**How Much Cache Do We Need?**

**Strategy: Cache 20% of Daily Traffic**

Based on our capacity estimation:
- **Daily requests:** 1.7 billion redirects/day
- **20% of daily traffic:** 0.2 × 1.7B = 340M requests
- **Cache size needed:** 170GB (as calculated in Step 2)

**Cache Server Capacity:**

**Option 1: Single Large Server**
- Modern server can have **256GB memory**
- Can easily fit all 170GB cache into one machine
- Simple to manage, single point of failure

**Option 2: Multiple Smaller Servers**
- Use a couple of smaller servers (e.g., 2 × 128GB = 256GB total)
- Better fault tolerance (if one fails, other continues)
- Can distribute load across servers

**Recommendation:**
- Start with **2-3 cache servers** (e.g., 3 × 64GB = 192GB total)
- Provides redundancy and load distribution
- Can scale up as traffic grows

**Cache Eviction Policy: LRU (Least Recently Used)**

**What is LRU?**
- When cache is full and we want to add a new URL, we need to evict an old one
- **LRU evicts the least recently used URL first**
- Keeps the most recently accessed URLs in cache

**Why LRU for URL Shortener?**

**Benefits:**
- ✅ **Keeps hot URLs:** Frequently accessed URLs stay in cache
- ✅ **Evicts cold URLs:** Rarely accessed URLs are removed
- ✅ **Matches access patterns:** URLs accessed recently are likely to be accessed again
- ✅ **Simple and effective:** Well-understood algorithm, good performance

**Example:**
```
Cache capacity: 3 URLs
Current cache: [URL-A, URL-B, URL-C] (oldest to newest)

Request 1: Access URL-A
Cache: [URL-B, URL-C, URL-A] (URL-A moved to end)

Request 2: Access URL-D (cache full)
Cache: [URL-C, URL-A, URL-D] (URL-B evicted, URL-D added)

Request 3: Access URL-C
Cache: [URL-A, URL-D, URL-C] (URL-C moved to end)
```

**Data Structure for LRU: Linked Hash Map**

**What is Linked Hash Map?**
- **Hash Map:** Fast O(1) lookup by key
- **Linked List:** Maintains insertion/access order
- **Combination:** Fast lookup + ordered tracking

**How Hash Map Works Internally (Buckets):**

**Important:** Hash map buckets are **NOT the same** as the consistent hashing ring we discussed earlier.

**Hash Map Internal Structure (Single Server):**

```
Hash Map with Buckets (Array of Buckets):
┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
│Bucket│ │Bucket│ │Bucket│ │Bucket│ │Bucket│
│  0   │ │  1   │ │  2   │ │  3   │ │ ... │
└───┬──┘ └───┬──┘ └───┬──┘ └───┬──┘ └───┬──┘
    │        │        │        │        │
    │        │        │        │        │
    ▼        ▼        ▼        ▼        ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Key: A │ │Key: B │ │Key: C │ │Key: D │
│Val:...│ │Val:...│ │Val:...│ │Val:...│
└───────┘ └───────┘ └───────┘ └───────┘
    │        │        │        │
    ▼        ▼        ▼        ▼
┌───────┐ ┌───────┐
│Key: E │ │Key: F │ (Collision - chaining)
│Val:...│ │Val:...│
└───────┘ └───────┘
```

**How It Works:**
1. **Hash Function:** `bucket_index = hash(key) % num_buckets`
2. **Bucket Array:** Array of buckets (e.g., 16, 32, 64, 128 buckets)
3. **Collision Handling:** If two keys hash to same bucket, use chaining (linked list in bucket)
4. **Lookup:** Hash key → find bucket → search in bucket (O(1) average, O(n) worst case)

**Example:**
```
Keys: "aBc123", "dEf456", "gHi789"
Hash("aBc123") % 16 = 3  → Bucket 3
Hash("dEf456") % 16 = 7  → Bucket 7
Hash("gHi789") % 16 = 3  → Bucket 3 (collision with "aBc123")

Bucket 3: [aBc123 → gHi789] (chained)
Bucket 7: [dEf456]
```

**Linked Hash Map Structure:**

**Combines Hash Map + Linked List:**

```
Hash Map (Buckets)          Linked List (Order)
┌─────┐                    ┌─────────┐    ┌─────────┐    ┌─────────┐
│Bucket│                    │ Key: A  │───▶│ Key: B  │───▶│ Key: C  │
│  0   │                    │ Val:... │    │ Val:... │    │ Val:... │
└───┬──┘                    └─────────┘    └─────────┘    └─────────┘
    │                           ↑              ↑              ↑
    ▼                           │              │              │
┌───────┐                      │              │              │
│Key: A │──────────────────────┘              │              │
│Val:...│                                      │              │
└───────┘                                      │              │
    │                                           │              │
    ▼                                           │              │
┌───────┐                                      │              │
│Key: B │──────────────────────────────────────┘              │
│Val:...│                                                     │
└───────┘                                                     │
    │                                                          │
    ▼                                                          │
┌───────┐                                                     │
│Key: C │─────────────────────────────────────────────────────┘
│Val:...│
└───────┘
```

**Key Differences:**

| Aspect | Hash Map Buckets | Consistent Hashing Ring |
|--------|------------------|------------------------|
| **Purpose** | Store data in single server | Distribute data across multiple servers |
| **Structure** | Array of buckets | Circle (ring) with hash values |
| **Scale** | Single hash map instance | Multiple partitions/servers |
| **Collision** | Handled within bucket (chaining) | Keys assigned to different servers |
| **Use Case** | Fast lookup in one server | Distributed system partitioning |

**Operations:**
1. **Lookup:** O(1) - Hash map lookup (hash key → find bucket → search bucket)
2. **Insert:** O(1) - Add to hash map bucket and end of linked list
3. **Update (on access):** O(1) - Move to end of linked list (update order)
4. **Evict:** O(1) - Remove from hash map bucket and head of linked list

**Implementation:**
- **Memcached/Redis:** Built-in LRU support (automatic, uses hash map + linked list internally)
- **Custom implementation:** Use LinkedHashMap (Java) or OrderedDict (Python)
  - Both use hash map buckets internally for fast lookup
  - Both maintain linked list for order tracking

**Cache Replication**

**Why Replicate Cache?**

- ✅ **Load Distribution:** Spread read requests across multiple cache servers
- ✅ **Fault Tolerance:** If one cache server fails, others continue serving
- ✅ **Higher Throughput:** Multiple servers can handle more requests
- ✅ **Geographic Distribution:** Place cache servers in different regions

**Replication Strategy:**

**Multiple Cache Replicas:**
```
Cache Replica 1 (Server 1)
Cache Replica 2 (Server 2)
Cache Replica 3 (Server 3)
```

**Load Distribution:**
- App servers can read from any cache replica
- Load balancer distributes requests across replicas
- Each replica has same data (eventually consistent)

**How Cache Replicas Are Updated**

**Cache Update Strategy:**

**When Cache Miss Occurs:**
```
1. App server checks cache → Cache miss
2. App server queries backend database
3. Database returns URL mapping
4. App server updates cache (writes to cache)
5. Cache propagates update to all replicas
```

**Update Propagation:**

**Option 1: Write-Through (Synchronous)**
```
1. App server writes to cache
2. Cache writes to all replicas synchronously
3. Wait for all replicas to confirm
4. Return success to app server
```

**Pros:**
- ✅ All replicas have same data immediately
- ✅ Strong consistency

**Cons:**
- ⚠️ Slower (must wait for all replicas)
- ⚠️ If one replica fails, write fails

**Option 2: Write-Behind (Asynchronous) - Recommended**

```
1. App server writes to cache (primary)
2. Cache returns success immediately
3. Cache asynchronously propagates to replicas
4. Replicas update in background
```

**Pros:**
- ✅ Fast (doesn't wait for replicas)
- ✅ High availability (works even if replicas are slow)

**Cons:**
- ⚠️ Temporary inconsistency (replicas may be slightly behind)
- ⚠️ Acceptable for cache (eventual consistency is OK)

**Update Logic:**
```
When new entry added to cache:
1. Add entry to primary cache
2. Propagate to all cache replicas
3. If replica already has entry, ignore (idempotent)
4. If replica doesn't have entry, add it
```

**Cache Flow (Complete):**

```
User Request: GET /aBc123

1. App Server checks local cache (in-memory)
   └─> If hit: Return immediately (fastest)

2. App Server checks Redis/Memcached cache
   └─> If hit: Return and update local cache

3. App Server queries database (cache miss)
   └─> Database returns original_url

4. App Server updates cache:
   ├─> Write to primary cache
   ├─> Propagate to cache replicas (async)
   └─> Update local cache

5. App Server returns original_url to user
```

**Cache Architecture:**

```
                    ┌─────────────┐
                    │ App Server 1│
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌────▼────┐       ┌────▼────┐
   │ Cache   │       │ Cache   │       │ Cache   │
   │Replica 1│       │Replica 2│       │Replica 3│
   └────┬────┘       └────┬────┘       └────┬────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    ┌──────▼───────┐
                    │   Database   │
                    └──────────────┘
```

**Cache Configuration:**

**Cache Size:**
- **Per server:** 64GB (3 servers = 192GB total)
- **Can cache:** ~170GB of hot URLs (as calculated)

**Cache TTL (Time To Live):**
- **24 hours:** URLs don't change often
- **Can be longer:** URLs rarely change, can cache for days
- **Invalidation:** If URL is updated/deleted, invalidate cache entry

**Cache Hit Rate Target:**
- **Target:** >80% cache hit rate
- **Meaning:** 80% of requests served from cache
- **Benefit:** Reduces database load by 80%

**Monitoring:**
- **Cache hit rate:** Should be >80%
- **Cache miss rate:** Should be <20%
- **Cache latency:** Should be <1ms (p99)
- **Cache size:** Monitor memory usage, evict if needed

**Summary:**

| Aspect | Details |
|--------|---------|
| **Cache Solution** | Memcached or Redis |
| **Cache Size** | 170GB (20% of daily traffic) |
| **Cache Servers** | 2-3 servers (64GB each) |
| **Eviction Policy** | LRU (Least Recently Used) |
| **Data Structure** | Linked Hash Map |
| **Replication** | 3 cache replicas |
| **Update Strategy** | Write-behind (async propagation) |
| **Cache Hit Rate** | Target >80% |
| **Cache TTL** | 24 hours |

### 6.3 Database Sharding

**Sharding Key:** Hash of short URL
- `shard_id = hash(hash) % num_shards`
- Ensures even distribution
- Easy to determine which shard to query

**Read Replicas:**
- Each shard has 1 master (writes) + 3-5 replicas (reads)
- Read requests go to replicas
- Write requests go to master
- Replication lag: <100ms (acceptable for reads)

---

## Step 7: Data Partitioning and Replication

### 7.1 What is a Partition?

**Definition:**
A **partition** (also called a **shard**) is a **subset of data** stored on a **separate database server**. Instead of storing all data on one server, we **divide the data** and store different subsets on different servers.

**Simple Analogy:**
Think of a library with millions of books:
- **Without partitioning:** All books in one huge room (single server) - hard to find books, slow
- **With partitioning:** Books divided into multiple rooms (partitions) - easier to find, faster
  - Room 1: Books A-F
  - Room 2: Books G-L
  - Room 3: Books M-R
  - Room 4: Books S-Z

**In Database Terms:**
```
Single Server (No Partitioning):
┌─────────────────────────────────┐
│  All 30 Billion URLs            │
│  (Too much data, slow queries)  │
└─────────────────────────────────┘

Partitioned (256 Partitions):
┌──────────┐  ┌──────────┐  ┌──────────┐
│Partition │  │Partition │  │Partition │
│   0      │  │   1      │  │  ...    │
│~117M URLs│  │~117M URLs│  │~117M URLs│
└──────────┘  └──────────┘  └──────────┘
    ↓              ↓              ↓
Server 1      Server 2      Server 256
```

**Key Concepts:**

1. **Partition = Subset of Data + Database Server:**
   - Each partition contains a portion of the total data
   - Each partition runs on its own database server (or cluster)
   - Partitions are independent (can be on different machines, different locations)

2. **Partition Key:**
   - The **field used to determine which partition** a record belongs to
   - Example: For URL shortener, we use the **hash of the short key** as partition key
   - `partition_id = hash(short_key) % num_partitions`

3. **Partitioning Function:**
   - The **algorithm that determines** which partition a record goes to
   - Example: `hash(key) % 256` → determines partition 0-255

**Example:**
```
URL Record:
- short_key: "aBc123"
- original_url: "https://example.com/very/long/url"

Partitioning:
1. Hash the short_key: hash("aBc123") = 150
2. Determine partition: 150 % 256 = 150
3. Store in Partition 150 (on Server 150)

When reading:
1. Hash the short_key: hash("aBc123") = 150
2. Determine partition: 150 % 256 = 150
3. Query Partition 150 (on Server 150)
4. Find the record
```

**Benefits of Partitioning:**
- ✅ **Scalability:** Can add more partitions as data grows
- ✅ **Performance:** Smaller datasets per server = faster queries
- ✅ **Parallel processing:** Multiple servers can process requests simultaneously
- ✅ **Fault isolation:** Failure in one partition doesn't affect others
- ✅ **Storage limits:** Each server has limited storage, partitioning distributes load

**Partition vs Shard:**
- **Partition:** General term for dividing data
- **Shard:** Specific term used in distributed databases (like MongoDB, Cassandra)
- **In practice:** They mean the same thing - dividing data across multiple servers

### 7.2 Why Partitioning is Needed

**Problem:**
- We need to store **30 billion URLs** over 5 years
- Single database server cannot handle this scale
- Need to **divide data across multiple database servers** (partitions/sharding)

**Benefits of Partitioning:**
- ✅ **Horizontal scaling:** Add more servers as data grows
- ✅ **Better performance:** Smaller datasets per server = faster queries
- ✅ **Fault isolation:** Failure in one partition doesn't affect others
- ✅ **Parallel processing:** Multiple servers can process requests simultaneously
  - **With single partition:** All requests go to one server → locking, queuing, sequential processing
  - **With multiple partitions:** Different requests go to different partitions → no locking between partitions, true parallel processing

### 7.2 Partitioning Strategies

**a. Range-Based Partitioning**

**How It Works:**
- Partition data based on the **first letter** of the short key or hash
- Example: All keys starting with 'A' go to Partition 1, 'B' to Partition 2, etc.

**Example:**
```
Partition 1: Keys starting with 'A', 'B', 'C'
Partition 2: Keys starting with 'D', 'E', 'F'
Partition 3: Keys starting with 'G', 'H', 'I'
...
Partition 26: Keys starting with 'Z', '0', '1'
```

**Pros:**
- ✅ **Simple to understand:** Easy to determine which partition to use
- ✅ **Predictable:** Can always find data in a predictable manner
- ✅ **Range queries:** Easy to query ranges (e.g., all keys starting with 'A')

**Cons:**
- ❌ **Unbalanced partitions:** Some letters occur more frequently
  - Example: Many URLs might start with 'E' (overloads one partition)
  - Example: Few URLs start with 'X' (underutilized partition)
- ❌ **Hot spots:** Popular ranges can overload specific partitions
- ❌ **Difficult to rebalance:** Moving data between partitions is complex

**Example Problem:**
```
Partition for 'E': 500M URLs (overloaded!)
Partition for 'X': 10M URLs (underutilized)
→ Unbalanced load distribution
```

**b. Hash-Based Partitioning**

**How It Works:**
- Take **hash of the short key** (or original URL)
- Use hash value to determine partition number
- Hash function maps key to a number (e.g., 1-256)
- That number represents which partition to use

**Example:**
```python
# Hash function
partition_id = hash(short_key) % num_partitions

# Example
short_key = "aBc123"
hash_value = hash("aBc123") = 150
partition_id = 150 % 256 = 150
→ Store in Partition 150
```

**Pros:**
- ✅ **Even distribution:** Hash function distributes keys randomly
- ✅ **No hot spots:** Popular keys don't cluster in one partition
- ✅ **Predictable:** Same key always maps to same partition

**Cons:**
- ❌ **Still can have overloaded partitions:**
  - If one partition gets more popular keys by chance
  - Hash collisions can cluster in specific partitions
- ❌ **No range queries:** Can't easily query ranges
- ❌ **Rebalancing:** Adding/removing partitions requires rehashing all keys

**Example:**
```
Hash("aBc123") % 256 = 150 → Partition 150
Hash("dEf456") % 256 = 23  → Partition 23
Hash("gHi789") % 256 = 150 → Partition 150 (collision, but OK)
```

**c. Consistent Hashing (Best Solution)**

**How It Works:**
- **Hash ring:** Imagine a circle (ring) with hash values 0 to 2^64-1
- **Partitions (nodes):** Placed at positions on the ring (based on hash of node ID)
- **Keys:** Hashed and placed on the ring
- **Assignment:** Key belongs to the first node clockwise from its position

**Important: Hash Ring is NOT a Database**

**What the Hash Ring Is:**
- **Logical/Conceptual Structure:** The hash ring is a **mathematical concept**, not a physical database
- **Algorithm:** Implemented in **application code** or by the **database system itself**
- **Routing Mechanism:** Used to determine which partition/server to route requests to

**Where Data is Actually Stored:**
- **Regular Databases:** Each partition is a regular database (DynamoDB, Cassandra, MySQL, PostgreSQL, etc.)
- **Hash Ring is Just Logic:** The ring is used to calculate which database to use, but data is stored in normal database tables

**How Consistent Hashing Works in Practice:**

**1. Hash Ring (Logical Structure):**
```
Hash Ring (0 to 2^64-1):
    0
    |
    |  Node A (hash: 100)    ← Database Server A
    |  Node B (hash: 200)    ← Database Server B
    |  Node C (hash: 300)    ← Database Server C
    |
    2^64-1
```

**2. Application Code (Determines Partition):**
```python
# This is application logic, not a database
def get_partition(short_key):
    # Hash the key
    key_hash = hash(short_key)  # e.g., 150

    # Find first node clockwise on ring
    # (This is just a calculation, not querying a database)
    if key_hash <= 100:
        return "Node A"  # Database Server A
    elif key_hash <= 200:
        return "Node B"  # Database Server B
    elif key_hash <= 300:
        return "Node C"  # Database Server C
    else:
        return "Node A"  # Wraps around ring
```

**3. Actual Database (Stores Data):**
```
Node B (Database Server B):
┌─────────────────────────┐
│  Regular Database Table │
│  (DynamoDB/Cassandra/   │
│   MySQL/PostgreSQL)     │
│                         │
│  short_key | original   │
│  ----------|----------- │
│  aBc123    | https://...│
│  dEf456    | https://...│
│  ...                    │
└─────────────────────────┘
```

**Database Systems That Use Consistent Hashing:**

**1. Built-in Consistent Hashing (Automatic):**
- **DynamoDB:** Automatically uses consistent hashing internally
  - You specify partition key, DynamoDB handles the ring
  - No need to implement ring yourself

- **Cassandra:** Uses consistent hashing automatically
  - You specify partition key, Cassandra distributes using ring
  - Ring is managed by Cassandra cluster

- **Riak:** Uses consistent hashing for key distribution
  - Automatically handles ring management

**2. Manual Implementation (Application-Level):**
- **MySQL/PostgreSQL:** You implement consistent hashing in application code
  - Application calculates which database server to use
  - Each server is a regular MySQL/PostgreSQL database
  - Hash ring logic is in your application, not in database

**Example: Manual Implementation with MySQL:**

```python
# Application code (not a database)
class ConsistentHashRing:
    def __init__(self, nodes):
        self.nodes = nodes  # List of database servers
        self.ring = {}
        # Place each node on ring based on hash of node ID
        for node in nodes:
            node_hash = hash(node.id) % (2**64)
            self.ring[node_hash] = node

    def get_node(self, key):
        # Hash the key
        key_hash = hash(key) % (2**64)

        # Find first node clockwise
        sorted_hashes = sorted(self.ring.keys())
        for node_hash in sorted_hashes:
            if key_hash <= node_hash:
                return self.ring[node_hash]
        # Wrap around
        return self.ring[sorted_hashes[0]]

# Usage
ring = ConsistentHashRing([
    MySQLServer("db1.example.com"),
    MySQLServer("db2.example.com"),
    MySQLServer("db3.example.com")
])

# Get which database to use (just a calculation)
db_server = ring.get_node("aBc123")  # Returns MySQLServer("db2.example.com")

# Now query the actual database
result = db_server.query("SELECT * FROM urls WHERE short_key = 'aBc123'")
```

**Summary:**

| Component | What It Is | Where It Lives |
|-----------|------------|----------------|
| **Hash Ring** | Logical structure (mathematical concept) | Application code or database system |
| **Partition Calculation** | Algorithm to determine which partition | Application code or database system |
| **Actual Data Storage** | Real database tables with URLs | Regular databases (DynamoDB, Cassandra, MySQL, etc.) |
| **Node Positions** | Hash values on the ring | Stored in application config or database metadata |

**Key Point:**
- The **hash ring is not a database** - it's a **routing mechanism**
- The **actual data** is stored in **regular databases** (one per partition)
- Consistent hashing is just the **algorithm** used to determine which database to query

**Benefits:**
- ✅ **Even distribution:** Keys distributed evenly across partitions
- ✅ **Minimal rebalancing:** When adding/removing partitions, only nearby keys move
- ✅ **No single point of failure:** Each partition can have replicas
- ✅ **Handles hot spots:** Can add more replicas for popular partitions

**Example:**
```
Hash Ring (0 to 2^64-1):
    0
    |
    |  Key "abc123" (hash: 150)
    |  └─> First node clockwise: Node B
    |
    |  Node A (hash: 100)
    |  Node B (hash: 200) ← Key assigned here
    |  Node C (hash: 300)
    |
    2^64-1
```

**When Partition is Added:**
- Only keys between old and new partition positions need to move
- Example: If Node D added at hash 250, only keys between 200-250 move
- **Minimal data movement** compared to hash-based partitioning

**When Partition is Removed:**
- Keys from removed partition move to next partition clockwise
- Example: If Node B removed, keys 100-200 move to Node C
- **Controlled data movement**

### 7.3 Partitioning for URL Shortener

**Main Database (URL Mappings) - Partitioning Strategy:**

**Choice: Consistent Hashing**

**Why:**
- ✅ Even distribution of 30 billion URLs
- ✅ Easy to add/remove partitions as data grows
- ✅ Minimal rebalancing when scaling

**Partitioning Key:**
- **Hash of short_key** (e.g., "aBc123")
- `partition_id = consistent_hash(short_key)`

**Number of Partitions:**
- **Initial:** 256 partitions (can scale to 1024+ as needed)
- **Reason:** 30B URLs ÷ 256 = ~117M URLs per partition (manageable)
- **Each partition:** Can handle ~117M URLs efficiently

**Partition Distribution:**
```
Partition 0:  Hash range 0x0000...0000 to 0x0100...0000
Partition 1:  Hash range 0x0100...0000 to 0x0200...0000
...
Partition 255: Hash range 0xFF00...0000 to 0xFFFF...FFFF
```

**Key-DB (KGS Database) - Partitioning Strategy:**

**Choice: Range-Based Partitioning (Simpler for Key Management)**

**Why:**
- Keys are pre-generated and sequential
- Easier to manage key generation per partition
- Can pre-generate keys in batches per partition

**Partitioning Key:**
- **First character of key** (or first few characters)
- Example: Keys starting with '0'-'9' → Partition 1, 'a'-'z' → Partition 2, etc.

**Number of Partitions:**
- **64 partitions** (one per Base64 character: A-Z, a-z, 0-9, +, /)
- **Reason:** 68.7B keys ÷ 64 = ~1.07B keys per partition
- **Each partition:** ~1.07B keys (manageable for key-DB)

**Alternative: Hash-Based for Key-DB**
- Can also use hash-based partitioning
- `partition_id = hash(key) % 64`
- More even distribution, but slightly more complex

### 7.4 Replication Strategy

**Why Replication:**
- ✅ **High availability:** If one server dies, replicas can serve requests
- ✅ **Read scaling:** Distribute read requests across replicas
- ✅ **Fault tolerance:** Data survives server failures
- ✅ **Geographic distribution:** Replicas in different availability zones

**Replication Architecture:**

**Main Database (URL Mappings):**

**Replication Factor: 3 (1 Primary + 2 Replicas per Partition)**

**Per Partition:**
- **1 Primary (Master):** Handles all writes
- **2 Replicas (Read Replicas):** Handle reads, backup for writes
- **Total per partition:** 3 database servers

**Availability Zones:**
- **3 Availability Zones (AZs):** For fault tolerance
- **Distribution:**
  - Primary in AZ-1
  - Replica 1 in AZ-2
  - Replica 2 in AZ-3
- **Benefit:** If one AZ fails, data still available in other AZs

**Replication Method:**
- **Synchronous replication:** For primary → replica 1 (strong consistency)
- **Asynchronous replication:** For primary → replica 2 (better performance)
- **Replication lag:** <100ms (acceptable for reads)

**Total Database Servers:**
- **256 partitions × 3 replicas = 768 database servers**
- **Distribution:** 256 servers per availability zone

**Key-DB (KGS Database):**

**Replication Factor: 3 (1 Primary + 2 Replicas)**

**Per Partition:**
- **1 Primary:** Handles key generation and assignment
- **2 Replicas:** Backup, can take over if primary fails
- **Total per partition:** 3 database servers

**Availability Zones:**
- **3 Availability Zones:**
  - Primary in AZ-1
  - Replica 1 in AZ-2
  - Replica 2 in AZ-3

**Total Key-DB Servers:**
- **64 partitions × 3 replicas = 192 database servers**
- **Distribution:** 64 servers per availability zone

### 7.5 Failover Protection

**Main Database Failover:**

**Scenario 1: Primary Server Fails**

```
1. Health check detects primary failure
2. Promote Replica 1 to Primary (automatic failover)
3. Replica 2 now replicates from new Primary
4. App servers update connection to new Primary
5. Service continues with minimal downtime (<30 seconds)
```

**Scenario 2: Entire Availability Zone Fails**

**Important:** We only need **ONE primary per partition**, not multiple primaries.

**Before Failure:**
```
Partition 0:
  - Primary: AZ-1 (FAILED)
  - Replica 1: AZ-2
  - Replica 2: AZ-3

Partition 1:
  - Primary: AZ-1 (FAILED)
  - Replica 1: AZ-2
  - Replica 2: AZ-3

... (all 256 partitions follow same pattern)
```

**After Failure (Failover Process):**

```
1. Detect AZ failure (e.g., AZ-1 with all primaries)
2. For each partition, promote ONE replica to Primary
   - Strategy: Promote Replica 1 (from AZ-2) to Primary
   - Replica 2 (from AZ-3) remains as replica
3. Update routing to point to new primaries (now in AZ-2)
4. Service continues (may have some data loss if async replication lag)

Result:
Partition 0:
  - Primary: AZ-2 (promoted from Replica 1)
  - Replica 1: AZ-3 (remains replica, now replicates from AZ-2)

Partition 1:
  - Primary: AZ-2 (promoted from Replica 1)
  - Replica 1: AZ-3 (remains replica, now replicates from AZ-2)

... (all 256 partitions)
```

**Why Only One Primary Per Partition?**

- ✅ **Data Consistency:** Only one primary can accept writes (prevents conflicts)
- ✅ **Standard Replication:** One primary + replicas is the standard pattern
- ✅ **Simpler Management:** One write path per partition

**Alternative Strategy (Load Distribution):**

Instead of promoting all from AZ-2, we could distribute:
```
- Half of partitions: Promote from AZ-2
- Half of partitions: Promote from AZ-3
- This distributes load across both AZs
```

**Example:**
```
Partitions 0-127: Primary in AZ-2 (promoted from Replica 1)
Partitions 128-255: Primary in AZ-3 (promoted from Replica 2)
```

**Why This Alternative Might Be Better:**
- ✅ **Load Distribution:** Spreads write load across both AZs
- ✅ **Better Performance:** No single AZ handles all writes
- ✅ **Fault Tolerance:** If one AZ fails again, we still have primaries in the other

**Our Recommendation:**
- **Promote from AZ-2 only** (simpler, consistent)
- Or **distribute across AZ-2 and AZ-3** (better load balancing)
- Either way, **only ONE primary per partition**

**Key-DB Failover:**

**Scenario 1: KGS Primary Server Fails**

```
1. KGS standby replica detects primary failure
2. Standby KGS takes over (becomes new primary)
3. New primary KGS connects to key-DB replicas
4. If key-DB primary fails, promote replica to primary
5. KGS continues generating and assigning keys
```

**Scenario 2: Key-DB Partition Primary Fails**

```
1. Health check detects primary failure
2. Promote replica to primary (within same partition)
3. KGS updates connection to new primary
4. Key generation continues for that partition
```

### 7.6 Complete Architecture

**Main Database Architecture:**

```
┌─────────────────────────────────────────────────────────┐
│  Main Database (URL Mappings) - 256 Partitions          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Partition 0:                                           │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│    │ Primary      │  │ Replica 1   │  │ Replica 2   │  │
│    │ (AZ-1)       │  │ (AZ-2)      │  │ (AZ-3)      │  │
│    └─────────────┘  └─────────────┘  └─────────────┘  │
│                                                          │
│  Partition 1:                                           │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│    │ Primary      │  │ Replica 1   │  │ Replica 2   │  │
│    │ (AZ-1)       │  │ (AZ-2)      │  │ (AZ-3)      │  │
│    └─────────────┘  └─────────────┘  └─────────────┘  │
│                                                          │
│  ... (254 more partitions)                              │
│                                                          │
│  Partition 255:                                         │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│    │ Primary      │  │ Replica 1   │  │ Replica 2   │  │
│    │ (AZ-1)       │  │ (AZ-2)      │  │ (AZ-3)      │  │
│    └─────────────┘  └─────────────┘  └─────────────┘  │
│                                                          │
│  Total: 256 partitions × 3 replicas = 768 servers       │
└─────────────────────────────────────────────────────────┘
```

**Key-DB Architecture:**

```
┌─────────────────────────────────────────────────────────┐
│  Key-DB (KGS Database) - 64 Partitions                 │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Partition 0 (Keys '0'-'9'):                            │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│    │ Primary      │  │ Replica 1   │  │ Replica 2   │  │
│    │ (AZ-1)       │  │ (AZ-2)      │  │ (AZ-3)      │  │
│    └─────────────┘  └─────────────┘  └─────────────┘  │
│                                                          │
│  ... (63 more partitions)                                │
│                                                          │
│  Total: 64 partitions × 3 replicas = 192 servers        │
└─────────────────────────────────────────────────────────┘
```

### 7.7 Read/Write Operations

**Write Operation (URL Shortening):**

```
1. App server generates/gets short key
2. Hash short key: partition_id = consistent_hash(short_key)
3. Route to partition's primary (in AZ-1)
4. Write to primary
5. Primary replicates to:
   - Replica 1 (AZ-2) - synchronous
   - Replica 2 (AZ-3) - asynchronous
6. Return success to app server
```

**Read Operation (URL Redirect):**

```
1. User requests short URL: tinyurl.com/aBc123
2. Extract key: "aBc123"
3. Hash key: partition_id = consistent_hash("aBc123")
4. Route to partition's replica (for read scaling)
   - Can read from any replica (Replica 1 or Replica 2)
   - Load balancer distributes reads across replicas
5. Return original URL
6. If not found, return 404
```

**Key-DB Operations:**

```
1. KGS needs to load keys from unused_keys table
2. Determine partition (based on key range or hash)
3. Route to partition's primary
4. Read batch of keys
5. Move to used_keys table (atomic operation)
6. Replicate to replicas
```

### 7.8 Scaling Considerations

**Adding New Partitions:**

**Main Database:**
- Use consistent hashing: Add new partition to ring
- Only keys in affected range need to move
- Example: Add Partition 256, only keys between 255-256 move
- **Minimal data movement**

**Key-DB:**
- Can add new partitions for new key ranges
- Pre-generate keys for new partition
- **No data movement needed** (new partition starts empty)

**Removing Partitions:**

**Main Database:**
- Remove partition from consistent hash ring
- Keys from removed partition move to next partition clockwise
- **Controlled data movement**

**Key-DB:**
- Mark partition as read-only
- Stop assigning new keys from that partition
- **No immediate data movement** (keys already assigned)

### 7.9 Summary

**Main Database (URL Mappings):**
- **Partitioning:** Consistent hashing (256 partitions)
- **Replication:** 3 replicas per partition (1 primary + 2 replicas)
- **Total servers:** 768 (256 per AZ)
- **Failover:** Automatic promotion of replicas to primary

**Key-DB (KGS Database):**
- **Partitioning:** Range-based (64 partitions)
- **Replication:** 3 replicas per partition (1 primary + 2 replicas)
- **Total servers:** 192 (64 per AZ)
- **Failover:** KGS standby + database replica promotion

**Benefits:**
- ✅ **High availability:** 3x replication across 3 AZs
- ✅ **Fault tolerance:** Can survive AZ failures
- ✅ **Scalability:** Easy to add/remove partitions
- ✅ **Performance:** Even load distribution
- ✅ **Consistency:** Synchronous replication for critical data

## Step 8: Cache

**Note:** This section was previously in Step 6.2, but is now organized as a separate step to match the book's structure where Cache is Section 8.

### 8.1 Caching Strategy

**Why Caching is Needed:**

We can cache URLs that are frequently accessed to improve performance. Instead of hitting the backend database for every redirect request, we can quickly check if the cache has the desired URL.

**Benefits:**
- ✅ **Faster response times:** Cache lookups are much faster than database queries (<1ms vs 10-50ms)
- ✅ **Reduced database load:** Cache handles hot URLs, database handles cache misses
- ✅ **Better scalability:** Cache can handle much higher read throughput than database
- ✅ **Cost effective:** Memory is cheaper than database compute for read-heavy workloads

**What to Cache:**

- **Hot URLs:** URLs that are frequently accessed (20% generating 80% traffic)
- **Cache key:** `short_url:{hash}` (e.g., `short_url:aBc123`)
- **Cache value:** `original_url` (e.g., `https://example.com/very/long/url`)
- **Full URL mapping:** Store both short key and original URL for quick lookup

**Cache Solution:**

**Off-the-Shelf Solutions:**
- **Memcached:** Simple, fast, distributed memory caching
- **Redis:** More features (persistence, data structures, pub/sub)
- **Both are suitable:** For URL shortener, either works well

**How Much Cache Do We Need?**

**Strategy: Cache 20% of Daily Traffic**

Based on our capacity estimation:
- **Daily requests:** 1.7 billion redirects/day
- **20% of daily traffic:** 0.2 × 1.7B = 340M requests
- **Cache size needed:** 170GB (as calculated in Step 2)

**Cache Server Capacity:**

**Option 1: Single Large Server**
- Modern server can have **256GB memory**
- Can easily fit all 170GB cache into one machine
- Simple to manage, single point of failure

**Option 2: Multiple Smaller Servers**
- Use a couple of smaller servers (e.g., 2 × 128GB = 256GB total)
- Better fault tolerance (if one fails, other continues)
- Can distribute load across servers

**Recommendation:**
- Start with **2-3 cache servers** (e.g., 3 × 64GB = 192GB total)
- Provides redundancy and load distribution
- Can scale up as traffic grows

**Cache Eviction Policy: LRU (Least Recently Used)**

**What is LRU?**
- When cache is full and we want to add a new URL, we need to evict an old one
- **LRU evicts the least recently used URL first**
- Keeps the most recently accessed URLs in cache

**Why LRU for URL Shortener?**

**Benefits:**
- ✅ **Keeps hot URLs:** Frequently accessed URLs stay in cache
- ✅ **Evicts cold URLs:** Rarely accessed URLs are removed
- ✅ **Matches access patterns:** URLs accessed recently are likely to be accessed again
- ✅ **Simple and effective:** Well-understood algorithm, good performance

**Example:**
```
Cache capacity: 3 URLs
Current cache: [URL-A, URL-B, URL-C] (oldest to newest)

Request 1: Access URL-A
Cache: [URL-B, URL-C, URL-A] (URL-A moved to end)

Request 2: Access URL-D (cache full)
Cache: [URL-C, URL-A, URL-D] (URL-B evicted, URL-D added)

Request 3: Access URL-C
Cache: [URL-A, URL-D, URL-C] (URL-C moved to end)
```

**Data Structure for LRU: Linked Hash Map**

**What is Linked Hash Map?**
- **Hash Map:** Fast O(1) lookup by key
- **Linked List:** Maintains insertion/access order
- **Combination:** Fast lookup + ordered tracking

**How Hash Map Works Internally (Buckets):**

**Important:** Hash map buckets are **NOT the same** as the consistent hashing ring we discussed earlier.

**Hash Map Internal Structure (Single Server):**

```
Hash Map with Buckets (Array of Buckets):
┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
│Bucket│ │Bucket│ │Bucket│ │Bucket│ │Bucket│
│  0   │ │  1   │ │  2   │ │  3   │ │ ... │
└───┬──┘ └───┬──┘ └───┬──┘ └───┬──┘ └───┬──┘
    │        │        │        │        │
    │        │        │        │        │
    ▼        ▼        ▼        ▼        ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Key: A │ │Key: B │ │Key: C │ │Key: D │
│Val:...│ │Val:...│ │Val:...│ │Val:...│
└───────┘ └───────┘ └───────┘ └───────┘
    │        │        │        │
    ▼        ▼        ▼        ▼
┌───────┐ ┌───────┐
│Key: E │ │Key: F │ (Collision - chaining)
│Val:...│ │Val:...│
└───────┘ └───────┘
```

**How It Works:**
1. **Hash Function:** `bucket_index = hash(key) % num_buckets`
2. **Bucket Array:** Array of buckets (e.g., 16, 32, 64, 128 buckets)
3. **Collision Handling:** If two keys hash to same bucket, use chaining (linked list in bucket)
4. **Lookup:** Hash key → find bucket → search in bucket (O(1) average, O(n) worst case)

**Example:**
```
Keys: "aBc123", "dEf456", "gHi789"
Hash("aBc123") % 16 = 3  → Bucket 3
Hash("dEf456") % 16 = 7  → Bucket 7
Hash("gHi789") % 16 = 3  → Bucket 3 (collision with "aBc123")

Bucket 3: [aBc123 → gHi789] (chained)
Bucket 7: [dEf456]
```

**Linked Hash Map Structure:**

**Combines Hash Map + Linked List:**

```
Hash Map (Buckets)          Linked List (Order)
┌─────┐                    ┌─────────┐    ┌─────────┐    ┌─────────┐
│Bucket│                    │ Key: A  │───▶│ Key: B  │───▶│ Key: C  │
│  0   │                    │ Val:... │    │ Val:... │    │ Val:... │
└───┬──┘                    └─────────┘    └─────────┘    └─────────┘
    │                           ↑              ↑              ↑
    ▼                           │              │              │
┌───────┐                      │              │              │
│Key: A │──────────────────────┘              │              │
│Val:...│                                      │              │
└───────┘                                      │              │
    │                                           │              │
    ▼                                           │              │
┌───────┐                                      │              │
│Key: B │──────────────────────────────────────┘              │
│Val:...│                                                     │
└───────┘                                                     │
    │                                                          │
    ▼                                                          │
┌───────┐                                                     │
│Key: C │─────────────────────────────────────────────────────┘
│Val:...│
└───────┘
```

**Key Differences:**

| Aspect | Hash Map Buckets | Consistent Hashing Ring |
|--------|------------------|------------------------|
| **Purpose** | Store data in single server | Distribute data across multiple servers |
| **Structure** | Array of buckets | Circle (ring) with hash values |
| **Scale** | Single hash map instance | Multiple partitions/servers |
| **Collision** | Handled within bucket (chaining) | Keys assigned to different servers |
| **Use Case** | Fast lookup in one server | Distributed system partitioning |

**Operations:**
1. **Lookup:** O(1) - Hash map lookup (hash key → find bucket → search bucket)
2. **Insert:** O(1) - Add to hash map bucket and end of linked list
3. **Update (on access):** O(1) - Move to end of linked list (update order)
4. **Evict:** O(1) - Remove from hash map bucket and head of linked list

**Implementation:**
- **Memcached/Redis:** Built-in LRU support (automatic, uses hash map + linked list internally)
- **Custom implementation:** Use LinkedHashMap (Java) or OrderedDict (Python)
  - Both use hash map buckets internally for fast lookup
  - Both maintain linked list for order tracking

**Cache Replication**

**Why Replicate Cache?**

- ✅ **Load Distribution:** Spread read requests across multiple cache servers
- ✅ **Fault Tolerance:** If one cache server fails, others continue serving
- ✅ **Higher Throughput:** Multiple servers can handle more requests
- ✅ **Geographic Distribution:** Place cache servers in different regions

**Replication Strategy:**

**Multiple Cache Replicas:**
```
Cache Replica 1 (Server 1)
Cache Replica 2 (Server 2)
Cache Replica 3 (Server 3)
```

**Load Distribution:**
- App servers can read from any cache replica
- Load balancer distributes requests across replicas
- Each replica has same data (eventually consistent)

**How Cache Replicas Are Updated**

**Cache Update Strategy:**

**When Cache Miss Occurs:**
```
1. App server checks cache → Cache miss
2. App server queries backend database
3. Database returns URL mapping
4. App server updates cache (writes to cache)
5. Cache propagates update to all replicas
```

**Update Propagation:**

**Option 1: Write-Through (Synchronous)**
```
1. App server writes to cache
2. Cache writes to all replicas synchronously
3. Wait for all replicas to confirm
4. Return success to app server
```

**Pros:**
- ✅ All replicas have same data immediately
- ✅ Strong consistency

**Cons:**
- ⚠️ Slower (must wait for all replicas)
- ⚠️ If one replica fails, write fails

**Option 2: Write-Behind (Asynchronous) - Recommended**

```
1. App server writes to cache (primary)
2. Cache returns success immediately
3. Cache asynchronously propagates to replicas
4. Replicas update in background
```

**Pros:**
- ✅ Fast (doesn't wait for replicas)
- ✅ High availability (works even if replicas are slow)

**Cons:**
- ⚠️ Temporary inconsistency (replicas may be slightly behind)
- ⚠️ Acceptable for cache (eventual consistency is OK)

**Update Logic:**
```
When new entry added to cache:
1. Add entry to primary cache
2. Propagate to all cache replicas
3. If replica already has entry, ignore (idempotent)
4. If replica doesn't have entry, add it
```

**Cache Flow (Complete):**

```
User Request: GET /aBc123

1. App Server checks local cache (in-memory)
   └─> If hit: Return immediately (fastest)

2. App Server checks Redis/Memcached cache
   └─> If hit: Return and update local cache

3. App Server queries database (cache miss)
   └─> Database returns original_url

4. App Server updates cache:
   ├─> Write to primary cache
   ├─> Propagate to cache replicas (async)
   └─> Update local cache

5. App Server returns original_url to user
```

**Cache Architecture:**

```
                    ┌─────────────┐
                    │ App Server 1│
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌────▼────┐       ┌────▼────┐
   │ Cache   │       │ Cache   │       │ Cache   │
   │Replica 1│       │Replica 2│       │Replica 3│
   └────┬────┘       └────┬────┘       └────┬────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    ┌──────▼───────┐
                    │   Database   │
                    └──────────────┘
```

**Cache Configuration:**

**Cache Size:**
- **Per server:** 64GB (3 servers = 192GB total)
- **Can cache:** ~170GB of hot URLs (as calculated)

**Cache TTL (Time To Live):**
- **24 hours:** URLs don't change often
- **Can be longer:** URLs rarely change, can cache for days
- **Invalidation:** If URL is updated/deleted, invalidate cache entry

**Cache Hit Rate Target:**
- **Target:** >80% cache hit rate
- **Meaning:** 80% of requests served from cache
- **Benefit:** Reduces database load by 80%

**Monitoring:**
- **Cache hit rate:** Should be >80%
- **Cache miss rate:** Should be <20%
- **Cache latency:** Should be <1ms (p99)
- **Cache size:** Monitor memory usage, evict if needed

**Summary:**

| Aspect | Details |
|--------|---------|
| **Cache Solution** | Memcached or Redis |
| **Cache Size** | 170GB (20% of daily traffic) |
| **Cache Servers** | 2-3 servers (64GB each) |
| **Eviction Policy** | LRU (Least Recently Used) |
| **Data Structure** | Linked Hash Map |
| **Replication** | 3 cache replicas |
| **Update Strategy** | Write-behind (async propagation) |
| **Cache Hit Rate** | Target >80% |
| **Cache TTL** | 24 hours |

## Step 9: Load Balancer (LB)

**Note:** According to the book's structure, Load Balancer is Section 9, after Cache (Section 8).

### 9.1 Why Load Balancing is Needed

Load balancing distributes incoming requests across multiple servers to:
- ✅ **Prevent overload:** No single server handles all traffic
- ✅ **Improve performance:** Distribute load evenly
- ✅ **High availability:** If one server fails, others continue serving
- ✅ **Scalability:** Easy to add more servers

### 9.2 Where to Place Load Balancers

We can add a Load Balancing layer at **three places** in our system:

**1. Between Clients and Application Servers**

```
Clients → Load Balancer → Application Servers
```

**Purpose:**
- Distribute incoming HTTP requests across multiple app servers
- Handle client connections (millions of clients)
- Route requests to healthy app servers

**Example:**
```
Client requests: 20K redirects/s
Load Balancer distributes to:
  - App Server 1: ~6.7K requests/s
  - App Server 2: ~6.7K requests/s
  - App Server 3: ~6.7K requests/s
```

**2. Between Application Servers and Database Servers**

```
Application Servers → Load Balancer → Database Servers (Read Replicas)
```

**Purpose:**
- Distribute database read requests across read replicas
- Route writes to primary database
- Balance load across database replicas

**Example:**
```
App Server needs to read URL:
Load Balancer routes to:
  - Database Replica 1 (Partition 150)
  - Database Replica 2 (Partition 150)
  - Database Replica 3 (Partition 150)

(Reads can go to any replica)
```

**3. Between Application Servers and Cache Servers**

```
Application Servers → Load Balancer → Cache Servers (Redis/Memcached)
```

**Purpose:**
- Distribute cache requests across multiple cache servers
- Route to available cache replicas
- Balance load across cache cluster

**Example:**
```
App Server needs to check cache:
Load Balancer routes to:
  - Cache Replica 1
  - Cache Replica 2
  - Cache Replica 3
```

### 9.3 Load Balancing Strategies

**1. Round Robin (Simple Approach)**

**How It Works:**
- Distributes incoming requests **equally** among backend servers
- Rotates through servers in order: Server 1 → Server 2 → Server 3 → Server 1 → ...

**Example:**
```
Request 1 → Server 1
Request 2 → Server 2
Request 3 → Server 3
Request 4 → Server 1
Request 5 → Server 2
...
```

**Benefits:**
- ✅ **Simple to implement:** Easy algorithm, no complex logic
- ✅ **No overhead:** Fast, minimal processing
- ✅ **Automatic failover:** If server is dead, LB removes it from rotation
- ✅ **Equal distribution:** Each server gets roughly same number of requests

**Limitations:**
- ⚠️ **Ignores server load:** Doesn't consider if server is overloaded
- ⚠️ **Ignores server speed:** Doesn't consider if server is slow
- ⚠️ **Ignores request complexity:** Simple requests and complex requests treated same

**Problem with Round Robin:**

**Scenario:**
```
Server 1: Overloaded (CPU 90%, slow response)
Server 2: Normal (CPU 40%, fast response)
Server 3: Normal (CPU 45%, fast response)

Round Robin still sends:
Request 1 → Server 1 (overloaded!)
Request 2 → Server 2
Request 3 → Server 3
Request 4 → Server 1 (overloaded again!)
...
```

**Result:** Server 1 gets overwhelmed, requests timeout, poor user experience

**2. Intelligent Load Balancing (Advanced Approach)**

**How It Works:**
- **Periodically queries** backend servers about their load
- **Adjusts traffic** based on server health and load
- Routes requests to servers with lowest load/fastest response

**Metrics to Consider:**
- **CPU usage:** Server with lower CPU gets more requests
- **Memory usage:** Server with more free memory gets more requests
- **Response time:** Server with faster response gets more requests
- **Active connections:** Server with fewer connections gets more requests
- **Health status:** Only route to healthy servers

**Example:**
```
Server 1: CPU 90%, Response 500ms → Few requests
Server 2: CPU 40%, Response 50ms  → More requests
Server 3: CPU 45%, Response 60ms  → More requests

Load Balancer routes:
Request 1 → Server 2 (lowest load)
Request 2 → Server 3 (low load)
Request 3 → Server 2 (lowest load)
Request 4 → Server 3 (low load)
Request 5 → Server 1 (only if others busy)
```

**Benefits:**
- ✅ **Considers server load:** Routes to less loaded servers
- ✅ **Better performance:** Faster servers get more requests
- ✅ **Prevents overload:** Avoids sending requests to overloaded servers
- ✅ **Adaptive:** Adjusts as server conditions change

**Trade-offs:**
- ⚠️ **More complex:** Requires health checks and metrics collection
- ⚠️ **Slight overhead:** Periodic queries add some overhead
- ⚠️ **Configuration needed:** Need to set thresholds and policies

### 9.4 Load Balancing Algorithms

**1. Round Robin:**
- Rotate through servers in order
- Simple, equal distribution

**2. Least Connections:**
- Route to server with fewest active connections
- Good for long-lived connections

**3. Least Response Time:**
- Route to server with fastest response time
- Good for performance optimization

**4. Weighted Round Robin:**
- Assign weights to servers (e.g., Server 1: weight 3, Server 2: weight 1)
- More powerful servers get more requests

**5. IP Hash:**
- Hash client IP to determine server
- Same client always goes to same server (session affinity)

### 9.5 Our Recommendation for URL Shortener

**Initial Setup (Simple):**
- **Round Robin** for all three layers
- Simple to implement and maintain
- Automatic failover (removes dead servers)
- Good enough for initial scale

**As System Grows (Advanced):**
- **Intelligent Load Balancing** for:
  - Client → App Servers (handle varying request complexity)
  - App Servers → Cache Servers (balance cache load)
- **Round Robin** for:
  - App Servers → Database Replicas (reads are similar complexity)

### 9.6 Load Balancer Implementation

**Options:**
1. **Hardware Load Balancer:** Dedicated hardware (F5, Citrix)
   - High performance, expensive

2. **Software Load Balancer:** Software solution (HAProxy, NGINX, AWS ELB)
   - Flexible, cost-effective
   - Recommended for URL shortener

**Example: HAProxy Configuration:**
```
# Round Robin
backend app_servers
    balance roundrobin
    server app1 10.0.1.1:8080 check
    server app2 10.0.2.1:8080 check
    server app3 10.0.3.1:8080 check

# Least Connections (Intelligent)
backend cache_servers
    balance leastconn
    server cache1 10.0.4.1:6379 check
    server cache2 10.0.4.2:6379 check
    server cache3 10.0.4.3:6379 check
```

### 9.7 Health Checks

**How It Works:**
- Load balancer periodically checks if servers are healthy
- If server fails health check, remove from rotation
- If server recovers, add back to rotation

**Health Check Methods:**
- **HTTP check:** Send HTTP request, check response
- **TCP check:** Check if port is open
- **Custom check:** Application-specific health endpoint

**Example:**
```
Health Check every 30 seconds:
- Server 1: ✅ Healthy (200 OK)
- Server 2: ✅ Healthy (200 OK)
- Server 3: ❌ Unhealthy (timeout) → Remove from rotation

After 30 seconds:
- Server 3: ✅ Healthy (200 OK) → Add back to rotation
```

**Summary:**

| Layer | Load Balancer Type | Algorithm | Purpose |
|-------|-------------------|-----------|---------|
| **Clients → App Servers** | Software (HAProxy/NGINX) | Round Robin (initial) or Least Connections (advanced) | Distribute HTTP requests |
| **App Servers → Database** | Database connection pool or proxy | Round Robin or Least Connections | Distribute database reads |
| **App Servers → Cache** | Cache cluster (Redis Cluster) | Round Robin or Least Connections | Distribute cache requests |

**Key Points:**
- ✅ **Start simple:** Round Robin is good for initial setup
- ✅ **Upgrade as needed:** Move to intelligent LB as system grows
- ✅ **Health checks:** Essential for automatic failover
- ✅ **Three layers:** Load balance at client, database, and cache layers

## Step 10: Purging or DB Cleanup

**Should entries stick around forever or should they be purged?**

**Problem:**
- URLs can have expiration times (user-specified or default)
- Expired links should not be returned to users
- Need to clean up expired links from database and cache
- Cleanup should not put pressure on database

### 10.1 Expiration Strategy

**Default Expiration:**
- **Default expiration time:** 2 years (if user doesn't specify)
- User can specify custom expiration when creating URL

**Lazy Cleanup (Recommended):**

**Why Not Active Cleanup?**
- ❌ **Active cleanup:** Searching for expired links puts a lot of pressure on database
- ✅ **Lazy cleanup:** Only remove expired links when accessed or during low-traffic periods
- ✅ **Service guarantee:** Only expired links will be deleted
- ✅ **Trade-off:** Some expired links may live longer in database, but will never be returned to users

### 10.2 Cleanup Mechanisms

**1. On-Access Cleanup**

**How It Works:**
- When user tries to access expired link, delete it and return error
- **Process:**
  ```
  1. User requests: GET /aBc123
  2. Check expiration_date in database
  3. If expired:
     - Delete from database
     - Remove from cache
     - Return 410 Gone (or 404 Not Found)
  4. If not expired: Return original URL
  ```

**2. Background Cleanup Service**

**How It Works:**
- **Separate Cleanup service** runs periodically
- Removes expired links from storage and cache
- Runs during **low-traffic periods** (e.g., 2 AM - 4 AM)
- **Lightweight:** Processes in batches (1000-10000 links), doesn't overload database

**Implementation:**
```python
# Pseudo-code for Cleanup Service
def cleanup_expired_links():
    batch_size = 1000

    while True:
        expired_links = db.get_expired_links(batch_size)
        if not expired_links:
            break

        for link in expired_links:
            db.delete(link.short_key)
            cache.delete(f"short_url:{link.short_key}")
            # Return key to key-DB (if using KGS)
            if using_kgs:
                kgs.return_key_to_pool(link.short_key)

        sleep(0.1)  # Rate limiting
```

**3. Hybrid Approach (Recommended)**
- **On-access cleanup:** Immediate deletion when user accesses expired link
- **Background cleanup:** Periodic cleanup during low-traffic hours
- **Best of both:** Immediate response + gradual cleanup

### 10.3 Key Reuse (If Using KGS)

**After Removing Expired Link:**
- **If using KGS:** Put the key back in key-DB (unused_keys table) to be reused
- **If using hash-based:** Keys are generated on-demand, no need to return to pool

### 10.4 Should We Remove Unvisited Links?

**Question:** Should we remove links that haven't been visited in some length of time (e.g., six months)?

**Recommendation: Keep Links Forever**
- ✅ **Storage is getting cheap:** Cost of storage is decreasing
- ✅ **User expectation:** Users expect links to work forever (unless expired)
- ✅ **Simplicity:** No need to track last access time
- ✅ **Only delete:** Links that have reached expiration date
- ✅ **Don't delete:** Based on last access time

**Exception:** If storage becomes a concern, can implement "unvisited" cleanup later, but for initial design, keep links forever.

## Step 11: Telemetry

**What Statistics to Track:**

- **Usage count:** How many times a short URL has been used
- **User locations:** Country of the visitor
- **Date and time:** When the URL was accessed
- **Referrer:** Web page that refers the click
- **Browser/Platform:** Browser or platform from where the page was accessed

**Example Statistics:**
```
- Short URL: "aBc123"
- Total clicks: 1,234,567
- Countries: US (60%), UK (20%), CA (10%), ...
- Last accessed: 2025-01-15 10:30:00
- Referrer: https://google.com (40%), https://twitter.com (30%), ...
- Browser: Chrome (50%), Safari (30%), Firefox (20%)
- Platform: Desktop (60%), Mobile (40%)
```

### 11.1 Storage Strategy

**Problem: Updating DB Row on Each View**

**If we store statistics in the same DB row:**
```
URLs table:
- short_key: "aBc123"
- original_url: "https://..."
- click_count: 1,234,567  ← Updated on every click
```

**Problem with Concurrent Requests:**
- Popular URL gets slammed with large number of concurrent requests
- Multiple requests try to update `click_count` simultaneously
- **Database locking:** Row-level locks cause contention
- **Performance degradation:** Updates become bottleneck
- **Race conditions:** May lose some click counts

**Example:**
```
Time | Request 1          | Request 2          | click_count
-----|-------------------|-------------------|-------------
T1   | Read: 1000        |                    | 1000
T2   |                   | Read: 1000         | 1000
T3   | Write: 1001       |                    | 1001
T4   |                   | Write: 1001       | 1001 (WRONG! Should be 1002)
```

**Solution: Separate Analytics Database**

**Strategy:**
- **Separate analytics database** for statistics (not in main URLs table)
- **Write-heavy workload:** Every redirect is logged (20K writes/s)
- **Async writes:** Don't block redirect response
- **No locking on main DB:** Main URLs table not updated on each view

**Architecture:**
```
User Request → App Server → Main DB (read only for redirect)
                    ↓
              Analytics DB (async write)
```

**Benefits:**
- ✅ **No contention:** Main DB not locked for statistics
- ✅ **Fast redirects:** Statistics don't slow down redirects
- ✅ **Scalable:** Analytics DB can scale independently
- ✅ **Flexible:** Can store detailed analytics without affecting main DB

### 11.2 Analytics Database Design

**Database Choice:**
- **NoSQL (MongoDB/Cassandra):** Flexible schema, good for write-heavy workloads
- **Time-series DB (InfluxDB):** Optimized for time-based analytics
- **DynamoDB:** Can use TTL for automatic cleanup

**Schema Example:**
```json
{
  "short_alias": "abc123",
  "clicked_at": "2025-01-15T10:30:00Z",
  "ip_address": "192.168.1.1",
  "country": "US",
  "referrer": "https://google.com",
  "user_agent": "Mozilla/5.0...",
  "platform": "Desktop",
  "browser": "Chrome"
}
```

**Aggregation:**
- **Real-time:** Update counters in Redis (for quick access)
- **Batch:** Aggregate hourly/daily in analytics DB
- **On-demand:** Generate reports when requested

### 11.3 Implementation

**Write Flow:**
```
1. User clicks short URL
2. App server redirects to original URL (fast response)
3. App server asynchronously writes analytics to analytics DB
   - Don't wait for analytics write to complete
   - Use message queue (Kafka, RabbitMQ) or async job
4. Analytics DB stores click event
```

**Read Flow (For Analytics Dashboard):**
```
1. User requests analytics: GET /api/v1/analytics/abc123
2. Query analytics DB (aggregated data)
3. Return statistics to user
```

**Benefits:**
- ✅ **Non-blocking:** Redirects are fast (don't wait for analytics)
- ✅ **Scalable:** Can handle high write volume
- ✅ **Accurate:** All clicks are logged (eventually)
- ✅ **Flexible:** Can add more statistics without affecting main DB

## Step 12: Security and Permissions

**Question:** Can users create private URLs or allow a particular set of users to access a URL?

**Answer:** Yes, we can support both public and private URLs with permission-based access control.

### 12.1 Permission Levels

**Two Types of URLs:**

1. **Public URLs:**
   - Anyone with the short URL can access it
   - No authentication required
   - Default behavior for most URLs

2. **Private URLs:**
   - Only specific users can access the URL
   - Requires permission check
   - Owner can grant/revoke access to specific users

**Example Use Cases:**
- **Public:** Marketing campaign links, social media shares
- **Private:** Internal company documents, personal files, restricted content

### 12.2 Database Design

**Option 1: Store Permission Level in URLs Table**

**Schema:**
```json
{
  "short_key": "abc123",
  "original_url": "https://example.com/private-doc",
  "user_id": "user_123",
  "permission_level": "private",  // "public" or "private"
  "created_at": "2025-01-15T10:00:00Z"
}
```

**Pros:**
- ✅ Simple: Single field indicates if URL is private
- ✅ Fast: One query to check permission level

**Cons:**
- ❌ Doesn't store which users have access (need separate table)

**Option 2: Separate Permissions Table (Recommended)**

**For NoSQL Wide-Column Database (Cassandra):**

**Permissions Table Structure:**
- **Key (Partition Key):** `short_key` (Hash or KGS-generated key)
- **Columns:** UserIDs that have permission to access the URL
- **Column Names:** UserID values
- **Column Values:** Permission metadata (optional: role, granted_at, etc.)

**Example in Cassandra:**
```
Permissions Table:
Key: "abc123"
Columns:
  - user_123: { role: "owner", granted_at: "2025-01-15T10:00:00Z" }
  - user_456: { role: "viewer", granted_at: "2025-01-15T11:00:00Z" }
  - user_789: { role: "viewer", granted_at: "2025-01-15T12:00:00Z" }
```

**For SQL Database:**

**Permissions Table:**
```sql
CREATE TABLE URL_Permissions (
    short_key VARCHAR(16) NOT NULL,
    user_id INT NOT NULL,
    role VARCHAR(20) DEFAULT 'viewer',  -- 'owner', 'viewer', 'editor'
    granted_at DATETIME NOT NULL,
    PRIMARY KEY (short_key, user_id),
    FOREIGN KEY (short_key) REFERENCES URLs(short_key),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
```

**For NoSQL Key-Value Store (DynamoDB):**

**Permissions Table:**
```json
{
  "short_key": "abc123",
  "user_id": "user_123",
  "role": "owner",
  "granted_at": "2025-01-15T10:00:00Z"
}
```
- **Partition Key:** `short_key`
- **Sort Key:** `user_id`

### 12.3 Access Control Flow

**1. URL Creation (POST /api/v1/urls)**

**Request:**
```json
POST /api/v1/urls
{
  "api_dev_key": "key_123",
  "original_url": "https://example.com/private-doc",
  "custom_alias": "my-private-link",
  "permission_level": "private",  // Optional, defaults to "public"
  "allowed_users": ["user_456", "user_789"]  // Optional, for private URLs
}
```

**Response:**
```json
{
  "short_url": "http://tinyurl.com/my-private-link",
  "permission_level": "private",
  "owner": "user_123"
}
```

**Database Operations:**
1. Insert URL into URLs table with `permission_level = "private"`
2. Insert owner into Permissions table (`user_123` with role `"owner"`)
3. Insert allowed users into Permissions table (`user_456`, `user_789` with role `"viewer"`)

**2. URL Access (GET /api/v1/{short_key})**

**Flow:**
```
1. User requests: GET /api/v1/abc123
2. Check if URL exists in URLs table
   - If not found → 404 Not Found
3. Check permission_level:
   - If "public" → Redirect to original_url (no auth needed)
   - If "private" → Check permissions
4. For private URLs:
   a. Get user_id from request (API key, session, etc.)
   b. Query Permissions table: Does user_id have access to short_key?
   c. If yes → Redirect to original_url
   d. If no → Return 401 Unauthorized
```

**Example:**
```python
def get_url(short_key, user_id):
    # 1. Get URL from database
    url_record = db.get_url(short_key)
    if not url_record:
        return 404, "URL not found"

    # 2. Check permission level
    if url_record.permission_level == "public":
        return 302, url_record.original_url  # Redirect

    # 3. For private URLs, check permissions
    if url_record.permission_level == "private":
        # Check if user has permission
        has_permission = db.check_permission(short_key, user_id)
        if not has_permission:
            return 401, "Unauthorized: You don't have permission to access this URL"

        return 302, url_record.original_url  # Redirect
```

**3. Grant/Revoke Permissions (PUT /api/v1/{short_key}/permissions)**

**Grant Permission:**
```json
PUT /api/v1/abc123/permissions
{
  "api_dev_key": "key_123",
  "action": "grant",
  "user_id": "user_999",
  "role": "viewer"
}
```

**Revoke Permission:**
```json
PUT /api/v1/abc123/permissions
{
  "api_dev_key": "key_123",
  "action": "revoke",
  "user_id": "user_999"
}
```

**Authorization Check:**
- Only URL owner (role = "owner") can grant/revoke permissions
- Verify `api_dev_key` matches URL owner before allowing changes

### 12.4 Error Handling

**HTTP 401 Unauthorized:**
- User tries to access private URL without permission
- User not authenticated (missing API key/session)
- User's API key doesn't match any user in Permissions table

**Response:**
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "You don't have permission to access this URL",
    "short_key": "abc123"
  }
}
```

**HTTP Status Code:** `401 Unauthorized`

### 12.5 Implementation Considerations

**For NoSQL Wide-Column Database (Cassandra):**

**Key Structure:**
- **Partition Key:** `short_key` (Hash or KGS-generated key)
- **Columns:** UserIDs (column names)
- **Column Values:** Permission metadata (role, granted_at, etc.)

**Query Pattern:**
```sql
-- Get all users with permission for a URL
SELECT * FROM Permissions WHERE short_key = 'abc123';

-- Check if specific user has permission
SELECT * FROM Permissions WHERE short_key = 'abc123' AND user_id = 'user_123';
```

**Benefits:**
- ✅ **Fast lookups:** Query by short_key to get all permissions
- ✅ **Scalable:** Wide-column stores handle many columns per row
- ✅ **Flexible:** Can add more permission metadata without schema changes

**For NoSQL Key-Value Store (DynamoDB):**

**Query Pattern:**
```python
# Get all permissions for a URL
permissions = dynamodb.query(
    TableName='Permissions',
    KeyConditionExpression='short_key = :key',
    ExpressionAttributeValues={':key': 'abc123'}
)

# Check if user has permission
permission = dynamodb.get_item(
    TableName='Permissions',
    Key={'short_key': 'abc123', 'user_id': 'user_123'}
)
```

### 12.6 Summary

**Key Points:**
- ✅ Store `permission_level` (public/private) in URLs table
- ✅ Use separate Permissions table to store UserIDs with access
- ✅ For NoSQL wide-column DB: Key = short_key, Columns = UserIDs
- ✅ Return HTTP 401 Unauthorized for unauthorized access
- ✅ Only URL owner can grant/revoke permissions
- ✅ Public URLs: No authentication required
- ✅ Private URLs: Check Permissions table before redirect

## Step 13: Additional Considerations

### 13.1 Rate Limiting and URL Validation

1. **Rate Limiting:**
   - Per `api_dev_key`: Limit URL creations and redirects
   - Per IP: Prevent abuse from single IP
   - Use Redis for distributed rate limiting

2. **URL Validation:**
   - Check URL format (must start with http:// or https://)
   - Block malicious URLs (phishing, malware)
   - Use URL blacklist service

**Note:** Detailed access control and permissions are covered in Step 12: Security and Permissions.

### 13.2 Analytics

**Note:** Detailed analytics/telemetry is covered in Step 11: Telemetry. This section provides a brief overview.

**Separate Analytics Database:**
- Write-heavy workload (every redirect is logged - 20K writes/s)
- Use NoSQL (MongoDB/Cassandra) or time-series DB (InfluxDB) for flexibility
- Store: click timestamp, IP, user agent, referrer, country
- Can use DynamoDB with TTL for automatic cleanup

**Analytics Schema:**
```json
{
  "short_alias": "abc123",
  "clicked_at": "2025-01-15T10:30:00Z",
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "referrer": "https://google.com",
  "country": "US"
}
```

**Aggregation:**
- Real-time: Update counters in Redis
- Batch: Aggregate hourly/daily in analytics DB
- Generate reports on-demand

### 13.3 Monitoring & Alerting

**Key Metrics:**
- QPS (Queries Per Second): Write and read
- Latency: p50, p95, p99 percentiles
- Error rates: 4xx, 5xx errors
- Cache hit rate: Should be >80%
- Database connection pool usage

**Alerts:**
- High error rate (>1%)
- High latency (p99 >500ms)
- Low cache hit rate (<70%)
- Database connection pool exhausted

### 13.4 Scaling Strategies

**Horizontal Scaling:**
- Add more application servers (stateless, easy to scale)
- Add more database shards (when single shard is too large)
- Add more Redis nodes (Redis cluster)

**Vertical Scaling:**
- Increase database server capacity (CPU, RAM, disk)
- Increase application server capacity

**Database Scaling:**
- **NoSQL:** Automatic partitioning and replication (DynamoDB/Cassandra)
- **Read replicas:** Scale reads (Cassandra reads from any replica)
- **Partitioning:** Automatic distribution across nodes
- **Connection pooling:** Reuse connections (if using connection-based DB)

---

## Step 14: Trade-offs & Alternatives

### 14.1 CAP Theorem and URL Shortener

**CAP Theorem:** In a distributed system, you can only guarantee **2 out of 3** properties:

1. **Consistency (C):** All nodes see the same data at the same time
2. **Availability (A):** System remains operational (every request gets a response)
3. **Partition Tolerance (P):** System continues despite network partitions

**URL Shortener's Choice: CP (Consistency + Partition Tolerance)**

**Why CP?**
- ✅ **Consistency is critical:** Cannot have duplicate short URLs (system breaks)
- ✅ **Partition tolerance required:** 256 partitions across 3 AZs, network partitions happen
- ⚠️ **Availability sacrificed:** May be unavailable during partitions or primary failures (<30 seconds)

**Implementation:**
- **Writes:** Synchronously replicate to at least one replica before returning success
- **Reads:** Can read from any replica (eventual consistency OK, <100ms lag acceptable)
- **Failover:** Automatic replica promotion (<30 seconds)

**CAP Choices by Component:**

| Component | CAP Choice | Reason |
|-----------|------------|--------|
| **Main Database** | **CP** | Cannot have duplicate URLs (consistency critical) |
| **Key-DB (KGS)** | **CP** | Cannot assign same key twice (consistency critical) |
| **Cache (Redis)** | **AP** | Stale data acceptable, high availability needed |
| **Analytics DB** | **AP** | High write volume (20K/s), stale data acceptable |

**Trade-offs:**
- **Main System (CP):** Better to be unavailable than return wrong data
- **Supporting Systems (AP):** Stale data is better than no data

### 14.2 Design Trade-offs

**Consistency vs Availability:**
- **Choice:** Strong consistency (CP)
- **Trade-off:** Service may be unavailable during partitions/failures

**Latency vs Cost:**
- **Choice:** Aggressive caching (<100ms redirects)
- **Trade-off:** Higher memory costs for better performance

**Complexity vs Performance:**
- **Choice:** Sharding (256 partitions)
- **Trade-off:** More complex to manage, but necessary for 30B URLs

### 14.3 Alternative Approaches

**Alternative: Pre-generate URL Hashes (KGS)**
- **Pros:** Fast assignment, batch generation
- **Cons:** Wastes unused hashes, complex pool management
- **Our Choice:** Hash-based with collision detection (no single point of failure, scales well)

---

## Summary

**Capacity:**
- **200 writes/s** (URL creations), **20K reads/s** (redirects)
- **30B URLs** over 5 years, **15TB storage**, **170GB cache**

**Key Features:**
- **Highly available** (redundant components, 3 replicas per partition)
- **Scalable** (256 partitions, horizontal scaling with NoSQL)
- **Fast** (caching for <100ms redirects)
- **Secure** (rate limiting, URL validation, permissions)

**Database:** NoSQL (DynamoDB/Cassandra/Riak) for billions of small, independent records

**Key Takeaways:**
1. Break down storage calculations field-by-field
2. Account for database overhead (metadata, indexes)
3. Use conservative estimates (round up)
4. Cache hot data to reduce database load
5. Choose database based on data characteristics (size, relationships, access patterns)
