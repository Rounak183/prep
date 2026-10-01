# Revision Notes - Key Patterns & Templates

## kSum Template

```python
def kSum(nums, target, k):
    """Time: O(n^(k-1)), Space: O(k)"""
    nums.sort()
    result = []

    def helper(start, target, k, path):
        if k == 2:
            left, right = start, len(nums) - 1
            while left < right:
                s = nums[left] + nums[right]
                if s < target: left += 1
                elif s > target: right -= 1
                else:
                    result.append(path + [nums[left], nums[right]])
                    left += 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
            return

        for i in range(start, len(nums) - k + 1):
            if i > start and nums[i] == nums[i - 1]:
                continue
            if nums[i] * k > target:
                break
            helper(i + 1, target - nums[i], k - 1, path + [nums[i]])

    helper(0, target, k, [])
    return result
```

**Complexity:** 2Sum O(n), 3Sum O(n²), 4Sum O(n³), kSum O(n^(k-1))

---

## Heap (Priority Queue) in Python

### Overview
Python's `heapq` module implements a **min-heap** (smallest element at root). For max-heap, negate values or use custom comparator.

### Basic Operations

```python
import heapq

# Create heap (list)
heap = []

# Push element
heapq.heappush(heap, 3)      # O(log n)
heapq.heappush(heap, 1)
heapq.heappush(heap, 2)
# heap = [1, 3, 2] (min-heap structure)

# Pop smallest element
smallest = heapq.heappop(heap)  # O(log n) - returns 1
# heap = [2, 3]

# Peek smallest (without removing)
smallest = heap[0]  # O(1) - returns 2

# Get largest element (for min-heap)
largest = heap[-1]  # O(1) - NOT guaranteed to be max! Only last element
```

### Key Functions

| Function | Time | Description |
|---------|------|-------------|
| `heappush(heap, item)` | O(log n) | Add element to heap |
| `heappop(heap)` | O(log n) | Remove and return smallest element |
| `heap[0]` | O(1) | Peek smallest element (min) |
| `heap[-1]` | O(1) | Last element (NOT max, just last in list) |
| `heapify(list)` | O(n) | Convert list to heap in-place |
| `heappushpop(heap, item)` | O(log n) | Push then pop (more efficient) |
| `heapreplace(heap, item)` | O(log n) | Pop then push (more efficient) |
| `nlargest(k, iterable)` | O(n log k) | Get k largest elements |
| `nsmallest(k, iterable)` | O(n log k) | Get k smallest elements |

### Important Notes

**⚠️ `heap[-1]` is NOT the maximum!**
- `heap[-1]` is just the last element in the list
- In a min-heap, the maximum could be anywhere
- To get max: use `max(heap)` O(n) or maintain separate max-heap

### Max-Heap Implementation

```python
# Method 1: Negate values
max_heap = []
heapq.heappush(max_heap, -5)  # Push -5
heapq.heappush(max_heap, -3)  # Push -3
max_val = -heapq.heappop(max_heap)  # Pop and negate: 5

# Method 2: Custom class
class MaxHeap:
    def __init__(self):
        self.heap = []

    def push(self, val):
        heapq.heappush(self.heap, -val)

    def pop(self):
        return -heapq.heappop(self.heap)

    def peek(self):
        return -self.heap[0]
```

### Heapify - Internal Working

```python
# Convert existing list to heap
nums = [3, 1, 4, 1, 5, 9, 2, 6]
heapq.heapify(nums)  # O(n) - modifies in-place
# nums is now a valid heap: [1, 1, 2, 3, 5, 9, 4, 6]
```

**How heapify works:**
- Starts from the last parent node (index `n//2 - 1`)
- Moves up the tree, "bubbling down" each node
- Time: O(n) - tighter bound than O(n log n) because:
  - Most nodes are at bottom levels (fewer swaps needed)
  - Only ~n/2 nodes need to be moved down
  - Average depth of nodes is much less than log n

### Internal Structure (Min-Heap)

```
Array representation: [1, 3, 2, 5, 4, 6, 7]
Tree structure:
          1
        /   \
       3     2
      / \   / \
     5   4 6   7

Index mapping:
- Parent of i: (i-1)//2
- Left child of i: 2*i + 1
- Right child of i: 2*i + 2
```

### Common Patterns

#### 1. K Largest/Smallest Elements

```python
# K smallest: O(n log k)
def k_smallest(nums, k):
    return heapq.nsmallest(k, nums)

# K largest: O(n log k)
def k_largest(nums, k):
    return heapq.nlargest(k, nums)

# Using heap: O(n log k) - better for large n, small k
def k_largest_heap(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap
```

#### 2. Two Heaps (Median, Sliding Window)

```python
# Find median from data stream
class MedianFinder:
    def __init__(self):
        self.small = []  # Max-heap (negated)
        self.large = []  # Min-heap

    def addNum(self, num):
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))

        if len(self.small) < len(self.large):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2
```

#### 3. Heap with Custom Comparator

```python
# Tuple comparison: (priority, value)
heap = []
heapq.heappush(heap, (2, 'task2'))
heapq.heappush(heap, (1, 'task1'))
heapq.heappush(heap, (3, 'task3'))
# Pops: (1, 'task1'), (2, 'task2'), (3, 'task3')

# Custom class
class Node:
    def __init__(self, val, priority):
        self.val = val
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

heap = []
heapq.heappush(heap, Node('B', 2))
heapq.heappush(heap, Node('A', 1))
```

### Time Complexity Summary

| Operation | Time | Notes |
|-----------|------|-------|
| `heappush` | O(log n) | Insert element |
| `heappop` | O(log n) | Remove min element |
| `heap[0]` | O(1) | Peek min |
| `heapify` | O(n) | Build heap from list |
| `heappushpop` | O(log n) | Push + pop (faster than separate) |
| `heapreplace` | O(log n) | Pop + push (faster than separate) |
| `nlargest(k, n)` | O(n log k) | k largest elements |
| `nsmallest(k, n)` | O(n log k) | k smallest elements |

### Space Complexity
- **Space:** O(n) for storing n elements

### Common Mistakes

1. **Using `heap[-1]` for max in min-heap** ❌
   - `heap[-1]` is just the last element, not guaranteed max
   - Use `max(heap)` O(n) or maintain max-heap

2. **Modifying heap elements directly** ❌
   ```python
   heap[0] = 10  # Breaks heap property!
   heapq.heapify(heap)  # Must re-heapify
   ```

3. **Using list methods that break heap property** ❌
   ```python
   heap.append(5)  # Wrong! Use heappush
   heap.sort()     # Wrong! Breaks heap structure
   ```

4. **Forgetting heap is min-heap by default**
   - For max-heap, negate values or use custom comparator

### Example: Merge K Sorted Lists

```python
def mergeKLists(lists):
    heap = []
    # Push first element of each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    result = []
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        # Push next element from same list
        if elem_idx + 1 < len(lists[list_idx]):
            heapq.heappush(heap, (lists[list_idx][elem_idx + 1],
                                 list_idx, elem_idx + 1))

    return result
```

---
