# FAANG Study Plan

## Week 1 (Jan 1-7): Arrays Foundation + BFS/DFS Basics + System Design Intro

**LeetCode: 18 problems, ~13 hours**
**System Design: 1 problem, ~2.5 hours**
**Total: ~15.5 hours**

### Arrays - Pattern 1-3 (11 problems, ~8 hours)

**Pattern 1: Two Pointers (5 problems)**

| #          | Problem                       | LeetCode #     | Difficulty     | Time      | Key Concept               | Revision     |
|------------|-------------------------------|----------------|----------------|-----------|---------------------------|--------------|
| Done 1     | 3Sum                          | 15             | Medium         | 45min     | Sort + two pointers       | 2            |
| Done 2     | 3Sum Closest                  | 16             | Medium         | 30min     | Variant of 3Sum           | 2            |
| Done 3     | Container With Most Water     | 11             | Medium         | 30min     | Greedy two pointers       | 2            |
| Done 4     | Trapping Rain Water           | 42             | Hard           | 60min     | Two pointers or stack     | 2            |
| Done 5     | Sort Colors (Dutch Flag)      | 75             | Medium         | 30min     | 3-way partitioning        | 2            |

**Pattern 2: Sliding Window (3 problems)**

| #          | Problem                                 | LeetCode #     | Difficulty     | Time      | Key Concept                | Revision     |
|------------|-----------------------------------------|----------------|----------------|-----------|----------------------------|--------------|
| Done 6     | Longest Substring Without Repeating     | 3              | Medium         | 45min     | Variable window + hash     | 2            |
| Done 7     | Minimum Window Substring                | 76             | Hard           | 60min     | Variable window            | 2            |
| Done 8     | Sliding Window Maximum                  | 239            | Hard           | 60min     | Deque/monotonic queue      | 2            |

**Pattern 3: Subarray Sum (3 problems)**

| #           | Problem                         | LeetCode #     | Difficulty     | Time      | Key Concept               | Revision     |
|-------------|---------------------------------|----------------|----------------|-----------|---------------------------|--------------|
| Done 9      | Maximum Subarray (Kadane's)     | 53             | Medium         | 30min     | Dynamic programming       | 1            |
| Done 10     | Maximum Product Subarray        | 152            | Medium         | 45min     | Track min and max         | 1            |
| Done 11     | Subarray Sum Equals K           | 560            | Medium         | 45min     | Prefix sum + hash map     | 1            |

### BFS/DFS Basics (4 problems, ~2.25 hours)

| #           | Problem                | LeetCode #     | Difficulty     | Time      | Key Concept                   | Revision     |
|-------------|------------------------|----------------|----------------|-----------|-------------------------------|--------------|
| Done 12     | Number of Islands      | 200            | Medium         | 45min     | DFS/BFS on grid               | 1            |
| Done 13     | Flood Fill             | 733            | Easy           | 20min     | DFS/BFS traversal             | 1            |
| Done 14     | Max Area of Island     | 695            | Medium         | 30min     | DFS with area calculation     | 1            |
| Done 15     | Rotting Oranges        | 994            | Medium         | 45min     | BFS multi-source              | 1            |

### Arrays Hard Problems (3 problems, ~2.75 hours)

| #           | Problem                          | LeetCode #     | Difficulty     | Time      | Key Concept       | Revision     |
|-------------|----------------------------------|----------------|----------------|-----------|-------------------|--------------|
| Done 16     | Median of Two Sorted Arrays      | 4              | Hard           | 60min     | Binary search     | 1            |
| Done 17     | Longest Consecutive Sequence     | 128            | Medium         | 45min     | Hash set          | 1            |
| Done 18     | Trapping Rain Water II           | 407            | Hard           | 60min     | Heap + BFS        | 1            |

### System Design

| #   | When                  | Problem                      | Time          | Notes                                                                                                                           |
|-----|-----------------------|------------------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------|
| D1  | Weekend (Jan 6-7)     | URL Shortening (TinyURL)     | 2.5 hours     | Use SYSTEM_DESIGN_TEMPLATE.md and URL_SHORTENER_EXAMPLE.md; follow all 8 steps, draw diagrams, calculate capacity estimates     |

**Weekend Review (Jan 6-7):**

| Task                                       |
|--------------------------------------------|
| Redo 3-5 LeetCode problems from Week 1     |
| Review URL Shortening system design        |

---

## Week 2 (Jan 8-14): Arrays Advanced + DFS Deep Dive + String Patterns + System Design

**LeetCode: 36 problems, ~27.75 hours**
**System Design: 2 problems, ~5 hours**
**Total: ~32.75 hours**

### Arrays - Pattern 4-8 (27 problems, ~20.5 hours)

**Pattern 4: Prefix Sum (2 problems)**

| #           | Problem                          | LeetCode #     | Difficulty     | Time      | Key Concept               | Revision     |
|-------------|----------------------------------|----------------|----------------|-----------|---------------------------|--------------|
| Done 19     | Product of Array Except Self     | 238            | Medium         | 30min     | Left × right products     | 1            |
| Done 20     | Continuous Subarray Sum          | 523            | Medium         | 45min     | Remainder + hash map      | 1            |

**Pattern 5: Intervals (4 problems)**

| #            | Problem               | LeetCode #     | Difficulty     | Time      | Key Concept                | Revision     |
|--------------|-----------------------|----------------|----------------|-----------|----------------------------|--------------|
| Done 21      | Merge Intervals       | 56             | Medium         | 45min     | Sort + merge               | 1            |
| Done 22      | Meeting Rooms I       | 252            | Easy           | 30min     | Check overlaps             | 1            |
| Done 23      | Meeting Rooms II      | 253            | Medium         | 45min     | Min heap or sweep line     | 1            |
| Done 24      | Meeting Rooms III     | 2402           | Hard           | 60min     | Heap + scheduling          | 1            |

**Pattern 6: Cyclic Sort (2 problems)**

| #           | Problem                          | LeetCode #     | Difficulty     | Time      | Key Concept       | Revision     |
|-------------|----------------------------------|----------------|----------------|-----------|-------------------|--------------|
| Done 25     | First Missing Positive           | 41             | Hard           | 60min     | Index as hash     | 1            |
| Done 26     | Find All Duplicates in Array     | 442            | Medium         | 30min     | Mark visited      | 1            |

**Pattern 7: Array Manipulation (11 problems)**

| #            | Problem              | LeetCode #     | Difficulty     | Time      | Key Concept                      | Revision     |
|--------------|----------------------|----------------|----------------|-----------|----------------------------------|--------------|
| Done 27      | Next Permutation     | 31             | Medium         | 45min     | Find pivot, reverse              | 1            |
| Done 28      | Rotate Array         | 189            | Medium         | 30min     | 3 reversals trick                | 1            |
| Done 29      | Jump Game            | 55             | Medium         | 30min     | Greedy                           | 2            |
| Done 30      | Jump Game II         | 45             | Medium         | 45min     | Greedy/DP - min jumps            | 2            |
| Done 31      | Jump Game III        | 1306           | Medium         | 45min     | BFS/DFS - reach zero             | 2            |
| Done 32      | Jump Game IV         | 1345           | Hard           | 60min     | BFS - same value jumps           | 2            |
| Done 33      | Jump Game V          | 1340           | Hard           | 60min     | DP with constraints              | 2            |
| Done 34      | Jump Game VI         | 1696           | Medium         | 45min     | DP + sliding window              | 2            |
| Done 35      | Jump Game VII        | 1871           | Medium         | 45min     | BFS with min/max constraints     | 1            |
| Done 36      | Jump Game VIII       | 2297           | Hard           | 60min     | Advanced DP/graph                |              |
| Done 37      | Jump Game IX         | 2463           | Hard           | 60min     | Advanced constraints             | 1            |

**Pattern 8: Stock Buy/Sell (8 problems)**

| #       | Problem                                       | LeetCode #     | Difficulty     | Time      | Key Concept                  | Revision |
|---------|-----------------------------------------------|----------------|----------------|-----------|------------------------------|----------|
| Done 38 | Best Time to Buy/Sell Stock                   | 121            | Easy           | 20min     | Track min, max profit        | 2        |
| Done 39 | Best Time II (Unlimited)                      | 122            | Medium         | 30min     | Greedy/DP                    | 2        |
| Done 40 | Best Time III (At Most 2)                     | 123            | Hard           | 60min     | State machine DP             | 2        |
| Done 41 | Best Time IV (At Most k)                      | 188            | Hard           | 60min     | DP with k transactions       | 1        |
| Done 42 | Best Time V (Normal + Short)                  | 3573           | Medium         | 60min     | DP with short selling        | 1        |
| Done 43 | Best Time with Cooldown                       | 309            | Medium         | 45min     | State machine (3 states)     | 1        |
| Done 44 | Best Time with Transaction Fee                | 714            | Medium         | 45min     | State machine + fee          | 1        |
| Done 45 | Best Time to But/Sell Stock with Strategy     | 309            | Medium         | 45min     |                              | 1        |

### DFS Advanced (3 problems, ~2.25 hours)

| #           | Problem                | LeetCode #     | Difficulty     | Time      | Key Concept             | Revision     |
|-------------|------------------------|----------------|----------------|-----------|-------------------------|--------------|
| Done 46     | Surrounded Regions     | 130            | Medium         | 45min     | DFS from boundaries     | 1            |
| Done 47     | Walls and Gates        | 286            | Medium         | 45min     | Multi-source BFS        | 1            |
| Done 48     | Word Search            | 79             | Medium         | 45min     | DFS backtracking        | 1            |

### String Patterns (3 problems, ~1.75 hours)

| #           | Problem                             | LeetCode #     | Difficulty     | Time      | Key Concept                  | Revision     |
|-------------|-------------------------------------|----------------|----------------|-----------|------------------------------|--------------|
| Done 49     | Valid Anagram                       | 242            | Easy           | 20min     | Hash map or sorting          | 1            |
| Done 50     | Group Anagrams                      | 49             | Medium         | 45min     | Hash map with sorted key     | 1            |
| Done 51     | Longest Palindromic Subsequence     | 516            | Medium         | 45min     | DP on strings                | 1            |

### Arrays Hard Problems (3 problems, ~3 hours)

| #       | Problem                          | LeetCode #     | Difficulty     | Time      | Key Concept                    | Revision |
|---------|----------------------------------|----------------|----------------|-----------|--------------------------------|----------|
| Done 52 | Merge k Sorted Lists             | 23             | Hard           | 60min     | Heap/divide and conquer        | 1        |
| Done 53 | Find Median from Data Stream     | 295            | Hard           | 60min     | Two heaps                      | 1        |
| Done 54 | Sliding Window Median            | 480            | Hard           | 60min     | Two heaps + sliding window     |          |

---

## Week 3 (Jan 15-21): DP Foundation + Graphs Basics + System Design

### DP - Pattern 1-4 (16 problems)

**Pattern 1: 1D DP - Classic Problems (5 problems)**

| #           | Problem                      | LeetCode #     | Difficulty     | Time      | Key Concept              | Revision     |
|-------------|------------------------------|----------------|----------------|-----------|--------------------------|--------------|
| Done 55     | Climbing Stairs              | 70             | Easy           | 20min     | Fibonacci pattern        | 1            |
| Done 56     | House Robber                 | 198            | Medium         | 30min     | Skip adjacent            | 1            |
| Done 57     | House Robber II              | 213            | Medium         | 45min     | Circular array           | 1            |
| Done 58     | Min Cost Climbing Stairs     | 746            | Easy           | 25min     | Choose min cost path     | 1            |
| Done 59     | Decode Ways                  | 91             | Medium         | 45min     | String DP                | 1            |

**Pattern 2: Coin Change & Unbounded Knapsack (4 problems)**

| #           | Problem             | LeetCode #     | Difficulty     | Time      | Key Concept             | Revision     |
|-------------|---------------------|----------------|----------------|-----------|-------------------------|--------------|
| Done 60     | Coin Change         | 322            | Medium         | 45min     | Min coins               | 1            |
| Done 61     | Coin Change 2       | 518            | Medium         | 45min     | Count combinations      | 1            |
| Done 62     | Perfect Squares     | 279            | Medium         | 30min     | Min squares             | 1            |
| Done 63     | Word Break          | 139            | Medium         | 45min     | String segmentation     | 1            |

**Pattern 3: 2D DP - Grid Problems (4 problems)**

| #            | Problem              | LeetCode #     | Difficulty     | Time      | Key Concept                            | Revision     |
|--------------|----------------------|----------------|----------------|-----------|----------------------------------------|--------------|
| Done 64      | Unique Paths         | 62             | Medium         | 30min     | Grid DP                                | 1            |
| Done 65      | Unique Paths II      | 63             | Medium         | 35min     | Handle obstacles                       | 1            |
| Done 66      | Minimum Path Sum     | 64             | Medium         | 35min     | Min cost path                          | 1            |
| Done 67      | Unique Paths III     | 980            | Hard           | 60min     | DFS/backtracking + visit all cells     | 1            |

**Pattern 4: Longest Common Subsequence (3 problems)**

| #           | Problem                        | LeetCode #     | Difficulty     | Time      | Key Concept               | Revision     |
|-------------|--------------------------------|----------------|----------------|-----------|---------------------------|--------------|
| Done 68     | Longest Common Subsequence     | 1143           | Medium         | 45min     | LCS classic               | 1            |
| Done 69     | Edit Distance                  | 72             | Hard           | 60min     | Insert/delete/replace     | 1            |
| Done 70     | Interleaving String            | 97             | Medium         | 45min     | String interleaving       | 1            |

### Graphs Basics - BFS/DFS (8 problems, ~6 hours)

| #            | Problem                         | LeetCode #     | Difficulty     | Time      | Key Concept                           | Revision     |
|--------------|---------------------------------|----------------|----------------|-----------|---------------------------------------|--------------|
| Done 71      | Clone Graph                     | 133            | Medium         | 45min     | DFS/BFS with mapping                  | 1            |
| Done 72      | Course Schedule                 | 207            | Medium         | 45min     | Cycle detection, topological sort     | 1            |
| Done 73      | Course Schedule II              | 210            | Medium         | 45min     | Topological sort ordering             | 1            |
| Done 74      | Course Schedule III             | 630            | Hard           | 60min     | Greedy + heap (duration/deadline)     | 1            |
| Done 75      | Course Schedule IV              | 1462           | Medium         | 45min     | Prerequisite checking, DFS/BFS        | 1            |
| Done 76      | Pacific Atlantic Water Flow     | 417            | Medium         | 45min     | Multi-source BFS/DFS                  | 1            |
| Done 77      | Is Graph Bipartite?             | 785            | Medium         | 45min     | Graph coloring, BFS/DFS               | 1            |
| Done 78      | Find the Town Judge             | 997            | Easy           | 30min     | Graph in/out degree                   | 1            |

### DP Hard Problems (3 problems, ~3 hours)

| #           | Problem                         | LeetCode #     | Difficulty     | Time      | Key Concept                | Revision     |
|-------------|---------------------------------|----------------|----------------|-----------|----------------------------|--------------|
| Done 79     | Regular Expression Matching     | 10             | Hard           | 60min     | String DP with * and .     | 1            |
| Done 80     | Wildcard Matching               | 44             | Hard           | 60min     | String DP with ? and *     | 1            |
| Done 81     | Dungeon Game                    | 174            | Hard           | 60min     | Reverse DP                 | 1            |

---

## Week 4 (Jan 22-28): DP Advanced + Graphs Advanced + Trees Foundation + System Design

### DP - Pattern 5-7 (9 problems, ~7.5 hours)

**Pattern 5: Longest Increasing Subsequence (3 problems)**

| #           | Problem                               | LeetCode #     | Difficulty     | Time      | Key Concept                | Revision     |
|-------------|---------------------------------------|----------------|----------------|-----------|----------------------------|--------------|
| Done 82     | Longest Increasing Subsequence        | 300            | Medium         | 45min     | O(n²) DP or O(n log n)     | 1            |
| Done 83     | Longest Increasing Path in Matrix     | 329            | Hard           | 60min     | DFS + memoization          | 1            |
| Done 84     | Russian Doll Envelopes                | 354            | Hard           | 60min     | Sort + LIS                 | 1            |

**Pattern 6: Palindrome DP (3 problems)**

| #           | Problem                           | LeetCode #     | Difficulty     | Time      | Key Concept               | Revision     |
|-------------|-----------------------------------|----------------|----------------|-----------|---------------------------|--------------|
| Done 85     | Longest Palindromic Substring     | 5              | Medium         | 45min     | Expand or DP              | 1            |
| Done 86     | Palindromic Substrings            | 647            | Medium         | 30min     | Count all palindromes     |              |
| 87          | Palindrome Partitioning II        | 132            | Hard           | 60min     | Min cuts                  |              |

**Pattern 7: Partition & Subset (3 problems)**

| #           | Problem                        | LeetCode #     | Difficulty     | Time      | Key Concept                | Revision     |
|-------------|--------------------------------|----------------|----------------|-----------|----------------------------|--------------|
| Done 88     | Partition Equal Subset Sum     | 416            | Medium         | 45min     | 0/1 knapsack               | 1            |
| Done 89     | Target Sum                     | 494            | Medium         | 45min     | Count ways                 | 1            |
| Done 90     | Word Break II                  | 140            | Hard           | 60min     | Generate all sentences     |              |

### Graphs Advanced (5 problems, ~4 hours)

| #           | Problem                             | LeetCode #     | Difficulty     | Time      | Key Concept                           | Revision     |
|-------------|-------------------------------------|----------------|----------------|-----------|---------------------------------------|--------------|
| Done 91     | Network Delay Time                  | 743            | Medium         | 45min     | Dijkstra's algorithm                  | 1            |
| Done 92     | Cheapest Flights Within K Stops     | 787            | Medium         | 45min     | BFS/Dijkstra variant                  |              |
| Done 93     | Redundant Connection                | 684            | Medium         | 45min     | Union-Find                            |              |
| 94          | Critical Connections                | 1192           | Hard           | 60min     | Tarjan's algorithm, bridges           |              |
| 95          | Find Eventual Safe States           | 802            | Medium         | 45min     | Topological sort, cycle detection     |              |

### Trees Foundation (9 problems, ~4.75 hours)

| #            | Problem                               | LeetCode #     | Difficulty     | Time      | Key Concept            | Revision     |
|--------------|---------------------------------------|----------------|----------------|-----------|------------------------|--------------|
| Done 96      | Maximum Depth of Binary Tree          | 104            | Easy           | 20min     | DFS recursion          | 1            |
| Done 97      | Same Tree                             | 100            | Easy           | 20min     | Tree comparison        | 1            |
| Done 98      | Binary Tree Level Order Traversal     | 102            | Medium         | 30min     | BFS on tree            | 1            |
| Done 99      | Binary Tree Zigzag Level Order        | 103            | Medium         | 45min     | BFS with direction     | 1            |
| Done 100     | Symmetric Tree                        | 101            | Easy           | 30min     | DFS comparison         | 1            |
| Done 101     | Invert Binary Tree                    | 226            | Easy           | 20min     | DFS recursion          | 1            |
| Done 102     | Path Sum                              | 112            | Easy           | 25min     | DFS with target        | 1            |
| Done 103     | Path Sum II                           | 113            | Medium         | 45min     | DFS backtracking       | 1            |
| Done 104     | Path Sum III                          | 437            | Medium         | 45min     | Prefix sum + DFS       |              |

### DP & Graphs Hard Problems (3 problems, ~3 hours)

| #      | Problem              | LeetCode #     | Difficulty     | Time      | Key Concept           | Revision     |
|--------|----------------------|----------------|----------------|-----------|-----------------------|--------------|
| 105    | Burst Balloons       | 312            | Hard           | 60min     | Range DP              |              |
| 106    | Scramble String      | 87             | Hard           | 60min     | Complex string DP     |              |
| 107    | Alien Dictionary     | 269            | Hard           | 60min     | Topological sort      |              |

---

## Week 5 (Jan 29 - Feb 7): Trees Advanced + Graphs Deep Dive + Backtracking + Trie + System Design

**LeetCode: 39 problems, ~31 hours**
**System Design: 1 problem, ~3 hours**
**Total: ~34 hours**

### Trees Advanced (9 problems, ~5.75 hours)

**Pattern 1: Tree Traversals (3 problems)**

| #           | Problem                             | LeetCode #     | Difficulty     | Time      | Key Concept             | Revision     |
|-------------|-------------------------------------|----------------|----------------|-----------|-------------------------|--------------|
| Done 108    | Binary Tree Inorder Traversal       | 94             | Medium         | 30min     | Iterative/recursive     | 1            |
| Done 109    | Binary Tree Preorder Traversal      | 144            | Medium         | 30min     | Iterative/recursive     | 1            |
| Done 110    | Binary Tree Postorder Traversal     | 145            | Hard           | 45min     | Iterative traversal     | 1            |

**Pattern 2: Binary Search Tree (4 problems)**

| #           | Problem                           | LeetCode #     | Difficulty     | Time      | Key Concept                 | Revision     |
|-------------|-----------------------------------|----------------|----------------|-----------|-----------------------------|--------------|
| Done 111    | Validate Binary Search Tree       | 98             | Medium         | 45min     | Inorder or bounds check     |              |
| Done 112    | Lowest Common Ancestor of BST     | 235            | Easy           | 30min     | BST property                |              |
| Done 113    | Kth Smallest Element in BST       | 230            | Medium         | 45min     | Inorder traversal           |              |
| Done 114    | Convert Sorted Array to BST       | 108            | Easy           | 30min     | Divide and conquer          |              |

**Pattern 3: Tree Construction (2 problems)**

| #           | Problem                                              | LeetCode #     | Difficulty     | Time      | Key Concept            | Revision     |
|-------------|------------------------------------------------------|----------------|----------------|-----------|------------------------|--------------|
| Done 115    | Construct Binary Tree from Preorder and Inorder      | 105            | Medium         | 45min     | Divide and conquer     |              |
| Done 116    | Construct Binary Tree from Inorder and Postorder     | 106            | Medium         | 45min     | Similar to #96         |              |

### Graphs Deep Dive (6 problems, ~5 hours)

**Pattern 1: Shortest Path (3 problems)**

| #            | Problem                                    | LeetCode #     | Difficulty     | Time      | Key Concept           | Revision     |
|--------------|--------------------------------------------|----------------|----------------|-----------|-----------------------|--------------|
| Done 117     | Path With Minimum Effort                   | 1631           | Medium         | 45min     | Dijkstra variant      | 1            |
| Done 118     | Shortest Path in Binary Matrix             | 1091           | Medium         | 45min     | BFS shortest path     | 1            |
| Done 119     | Shortest Path in a Grid with Obstacles     | 1293           | Hard           | 60min     | BFS with state        | 1            |

**Pattern 2: Union-Find & Connectivity (3 problems)**

| #            | Problem                            | LeetCode #     | Difficulty     | Time      | Key Concept                        | Revision     |
|--------------|------------------------------------|----------------|----------------|-----------|------------------------------------|--------------|
| Done 120     | Number of Connected Components     | 323            | Medium         | 45min     | Union-Find                         |              |
| 121          | Redundant Connection II            | 685            | Hard           | 60min     | Union-Find with directed graph     |              |
| Done 122     | Accounts Merge                     | 721            | Medium         | 45min     | Union-Find + hash map              |              |

### Backtracking Foundation (6 problems, ~4.25 hours)

**Pattern 1: Permutations & Combinations (3 problems)**

| #            | Problem             | LeetCode #     | Difficulty     | Time      | Key Concept               | Revision     |
|--------------|---------------------|----------------|----------------|-----------|---------------------------|--------------|
| Done 123     | Permutations        | 46             | Medium         | 45min     | Classic backtracking      | 1            |
| Done 124     | Permutations II     | 47             | Medium         | 45min     | Handle duplicates         | 1            |
| Done 125     | Combinations        | 77             | Medium         | 45min     | Generate combinations     | 1            |

**Pattern 2: Subsets & Generation (3 problems)**

| #            | Problem                  | LeetCode #     | Difficulty     | Time      | Key Concept                       | Revision     |
|--------------|--------------------------|----------------|----------------|-----------|-----------------------------------|--------------|
| Done 126     | Subsets                  | 78             | Medium         | 30min     | Generate all subsets              | 1            |
| Done 127     | Subsets II               | 90             | Medium         | 45min     | Handle duplicates                 | 1            |
| Done 128     | Generate Parentheses     | 22             | Medium         | 45min     | Backtracking with constraints     | 1            |

### Trie (Prefix Tree) (3 problems, ~2.5 hours)

| #            | Problem                          | LeetCode #     | Difficulty     | Time      | Key Concept                  | Revision     |
|--------------|----------------------------------|----------------|----------------|-----------|------------------------------|--------------|
| Done 129     | Implement Trie (Prefix Tree)     | 208            | Medium         | 45min     | Basic Trie operations        |              |
| Done 130     | Replace Words                    | 648            | Medium         | 45min     | Trie for prefix matching     |              |
| Done 131     | Word Search II                   | 212            | Hard           | 60min     | Trie + backtracking          |              |

### Trees Hard Problems (4 problems, ~4 hours)

| #            | Problem                                   | LeetCode #     | Difficulty     | Time      | Key Concept             | Revision     |
|--------------|-------------------------------------------|----------------|----------------|-----------|-------------------------|--------------|
| Done 132     | Serialize and Deserialize Binary Tree     | 297            | Hard           | 60min     | Tree traversal          |              |
| Done 133     | Binary Tree Maximum Path Sum              | 124            | Hard           | 60min     | Tree DP                 |              |
| Done 134     | Recover Binary Search Tree                | 99             | Hard           | 60min     | Inorder traversal       |              |
| Done 135     | Binary Tree Cameras                       | 968            | Hard           | 60min     | Tree DP with states     |              |

### Backtracking Hard Problems (2 problems, ~2 hours)

| #            | Problem           | LeetCode #     | Difficulty     | Time      | Key Concept                       | Revision     |
|--------------|-------------------|----------------|----------------|-----------|-----------------------------------|--------------|
| Done 136     | N-Queens          | 51             | Hard           | 60min     | Classic backtracking              |              |
| Done 137     | Sudoku Solver     | 37             | Hard           | 60min     | Backtracking with constraints     |              |

### Graphs Hard Problems (4 problems, ~4 hours)

| #            | Problem                                          | LeetCode #     | Difficulty     | Time      | Key Concept                | Revision     |
|--------------|--------------------------------------------------|----------------|----------------|-----------|----------------------------|--------------|
| 138          | Word Ladder II                                   | 126            | Hard           | 60min     | BFS + backtracking         |              |
| 139          | Reconstruct Itinerary                            | 332            | Hard           | 60min     | Eulerian path              |              |
| Done 140     | Minimum Cost to Make at Least One Valid Path     | 1368           | Hard           | 60min     | 0-1 BFS                    |              |
| 141          | Swim in Rising Water                             | 778            | Hard           | 60min     | Dijkstra or Union-Find     |              |

### Additional Hard Problems (5 problems, ~3.5 hours)

| #            | Problem                                   | LeetCode #     | Difficulty     | Time      | Key Concept                      | Revision     |
|--------------|-------------------------------------------|----------------|----------------|-----------|----------------------------------|--------------|
| Done 142     | Lowest Common Ancestor of Binary Tree     | 236            | Medium         | 45min     | DFS recursion                    |              |
| Done 143     | Binary Tree Right Side View               | 199            | Medium         | 30min     | BFS level order                  |              |
| Done 144     | Count Complete Tree Nodes                 | 222            | Medium         | 45min     | Binary search on tree            |              |
| Done 145     | N-Queens II                               | 52             | Hard           | 45min     | Count solutions                  |              |
| Done 146     | Restore IP Addresses                      | 93             | Medium         | 45min     | Backtracking with validation     |              |

---

## Summary

### LeetCode by Topic

| Topic            | Core | Hard | Total | Hours  |
|------------------|------|------|-------|--------|
| Arrays           | 28   | 16   | 44    | ~34.25 |
| DP               | 19   | 12   | 31    | ~23.25 |
| Graphs           | 15   | 9    | 24    | ~20    |
| Trees            | 20   | 5    | 25    | ~16.5  |
| Backtracking     | 7    | 3    | 10    | ~7.75  |
| Strings          | 3    | 0    | 3     | ~1.75  |
| Trie             | 2    | 1    | 3     | ~2.5   |
| BFS/DFS          | 7    | 0    | 7     | ~4.5   |
| Linked Lists     | 10   | 0    | 10    | ~7     |
| Stacks & Queues  | 7    | 1    | 8     | ~5.25  |
| Heaps            | 7    | 1    | 8     | ~6.25  |
| Binary Search    | 11   | 1    | 12    | ~9.5   |
| Bit Manipulation | 6    | 0    | 6     | ~3.25  |
| Greedy           | 6    | 0    | 6     | ~4.5   |
| Design           | 4    | 0    | 4     | ~3     |

### Grand Total (Weeks 1-5, Jan 1 - Feb 7)

| Component         | Week 1                    | Week 2                                | Week 3                               | Week 4                       | Week 5 (Jan 29 - Feb 7) | Total                          |
|-------------------|---------------------------|---------------------------------------|--------------------------------------|------------------------------|-------------------------|--------------------------------|
| LeetCode          | 18 (~13h)                 | 36 (~27.75h)                          | 27 (~19.75h)                         | 26 (~19.25h)                 | 39 (~31h)               | 146 problems, ~110.5 hours     |
| System Design     | D1 URL Shortening (2.5h)  | D2 Pastebin, D3 API Rate Limiter (5h) | D4 Typeahead, D5 Twitter Search (5h) | D6 Web Crawler, D7 Yelp (5h) | D8 Instagram (3h)       | 8 problems, ~20.5 hours        |

### February Continuation (System Design + LeetCode Practice)

**Remaining 7 System Design Problems:**

| Week                   | Problems                                                  | Hours     |
|------------------------|-----------------------------------------------------------|-----------|
| Week 1 (Feb 5-11)      | D9 Twitter, D10 Facebook Newsfeed, D11 Facebook Messenger | ~8-10     |
| Week 2 (Feb 12-18)     | D12 Dropbox, D13 Youtube/Netflix                          | ~7-8      |
| Week 3 (Feb 19-25)     | D14 Uber backend, D15 Ticketmaster                        | ~7-8      |
| Week 4 (Feb 26-28)     | System Design Basics Review                               | ~5-8      |

| Additional                                                         |
|--------------------------------------------------------------------|
| Continue LeetCode practice (Linked Lists, Heaps, Stacks, etc.)     |

---

## March Expansion (LeetCode Add-On, 50 Problems)

**Goal:** Solidify missing core topics before deeper system design ramp-up.
**March Mode Shift:** Starting March 1, switch from pattern blocks to random sets (LeetCode random/pick-one or mock platforms) to simulate interview conditions.

### Linked Lists (10 problems, ~7 hours)

| #            | Problem                      | LeetCode #     | Difficulty     | Time      | Key Concept                 | Revision     |
|--------------|------------------------------|----------------|----------------|-----------|-----------------------------|--------------|
| Done 147     | Reverse Linked List          | 206            | Easy           | 30min     | Pointer reversal            |              |
| Done 148     | Merge Two Sorted Lists       | 21             | Easy           | 30min     | Merge pointers              |              |
| Done 149     | Linked List Cycle            | 141            | Easy           | 30min     | Fast/slow pointers          |              |
| Done 150     | Linked List Cycle II         | 142            | Medium         | 45min     | Cycle entry                 |              |
| Done 151     | Remove Nth Node From End     | 19             | Medium         | 45min     | Two pointers                |              |
| Done 152     | Reorder List                 | 143            | Medium         | 60min     | Split + reverse + merge     |              |
| Done 153     | Palindrome Linked List       | 234            | Easy           | 30min     | Reverse second half         |              |
| 154          | Add Two Numbers              | 2              | Medium         | 45min     | Carry + traversal           |              |
| Done 155     | Swap Nodes in Pairs          | 24             | Medium         | 45min     | Pointer rewiring            |              |
| Done 156     | Sort List                    | 148            | Medium         | 60min     | Merge sort                  |              |

### Stacks & Queues (8 problems, ~5.25 hours)

| #            | Problem                              | LeetCode #     | Difficulty     | Time      | Key Concept         | Revision     |
|--------------|--------------------------------------|----------------|----------------|-----------|---------------------|--------------|
| Done 157     | Valid Parentheses                    | 20             | Easy           | 30min     | Stack matching      |              |
| Done 158     | Min Stack                            | 155            | Easy           | 30min     | Stack with min      |              |
| Done 159     | Implement Queue using Stacks         | 232            | Easy           | 30min     | Stack inversion     |              |
| Done 160     | Implement Stack using Queues         | 225            | Easy           | 30min     | Queue rotation      |              |
| Done 161     | Evaluate Reverse Polish Notation     | 150            | Medium         | 45min     | Stack eval          |              |
| Done 162     | Daily Temperatures                   | 739            | Medium         | 45min     | Monotonic stack     |              |
| Done 163     | Validate Stack Sequences             | 946            | Medium         | 45min     | Simulation          |              |
| 164          | Largest Rectangle in Histogram       | 84             | Hard           | 60min     | Monotonic stack     |              |

### Heaps / Priority Queue (8 problems, ~6.25 hours)

| #            | Problem                             | LeetCode #     | Difficulty     | Time      | Key Concept            | Revision     |
|--------------|-------------------------------------|----------------|----------------|-----------|------------------------|--------------|
| 165          | Kth Largest Element in an Array     | 215            | Medium         | 45min     | Heap/quickselect       |              |
| Done 166     | Kth Largest in a Stream             | 703            | Easy           | 30min     | Min-heap               |              |
| Done 167     | Top K Frequent Elements             | 347            | Medium         | 45min     | Heap/bucket            |              |
| Done 168     | K Closest Points to Origin          | 973            | Medium         | 45min     | Heap                   |              |
| Done 169     | Find K Pairs with Smallest Sums     | 373            | Medium         | 60min     | Heap + pairs           |              |
| 170          | Task Scheduler                      | 621            | Medium         | 45min     | Heap + greedy          |              |
| 171          | Reorganize String                   | 767            | Medium         | 45min     | Max-heap               |              |
| 172          | IPO                                 | 502            | Hard           | 60min     | Max-heap + capital     |              |

### Binary Search (12 problems, ~9.5 hours)

| #            | Problem                                     | LeetCode #     | Difficulty     | Time      | Key Concept             | Revision     |
|--------------|---------------------------------------------|----------------|----------------|-----------|-------------------------|--------------|
| Done 173     | Binary Search                               | 704            | Easy           | 30min     | Standard BS             |              |
| Done 174     | Search Insert Position                      | 35             | Easy           | 30min     | Bounds                  |              |
| Done 175     | Find First and Last Position of Element     | 34             | Medium         | 45min     | Two binary searches     |              |
| Done 176     | Search in Rotated Sorted Array              | 33             | Medium         | 45min     | Rotated BS              |              |
| Done 177     | Search in Rotated Sorted Array II           | 81             | Medium         | 45min     | Duplicates              |              |
| Done 178     | Find Minimum in Rotated Sorted Array        | 153            | Medium         | 45min     | Pivot search            |              |
| Done 179     | Find Peak Element                           | 162            | Medium         | 45min     | Peak BS                 |              |
| Done 180     | Search a 2D Matrix                          | 74             | Medium         | 45min     | Flattened BS            |              |
| Done 181     | Koko Eating Bananas                         | 875            | Medium         | 60min     | Answer space BS         |              |
| Done 182     | Capacity To Ship Packages Within D Days     | 1011           | Medium         | 60min     | Answer space BS         |              |
| Done 183     | Split Array Largest Sum                     | 410            | Hard           | 60min     | Answer space BS         |              |
| Done 184     | Kth Smallest Element in a Sorted Matrix     | 378            | Medium         | 60min     | Answer space BS         |              |

### Bit Manipulation (6 problems, ~3.25 hours)

| #            | Problem                 | LeetCode #     | Difficulty     | Time      | Key Concept     | Revision     |
|--------------|-------------------------|----------------|----------------|-----------|-----------------|--------------|
| Done 185     | Single Number           | 136            | Easy           | 30min     | XOR             |              |
| Done 186     | Number of 1 Bits        | 191            | Easy           | 30min     | Bit count       |              |
| 187          | Counting Bits           | 338            | Easy           | 30min     | DP + bits       |              |
| 188          | Reverse Bits            | 190            | Easy           | 30min     | Bit ops         |              |
| Done 189     | Missing Number          | 268            | Easy           | 30min     | XOR / math      |              |
| 190          | Sum of Two Integers     | 371            | Medium         | 45min     | Bitwise sum     |              |

### Greedy (6 problems, ~4.5 hours)

| #            | Problem                                        | LeetCode #     | Difficulty     | Time      | Key Concept            | Revision     |
|--------------|------------------------------------------------|----------------|----------------|-----------|------------------------|--------------|
| Done 191     | Gas Station                                    | 134            | Medium         | 45min     | Greedy feasibility     |              |
| Done 192     | Non-overlapping Intervals                      | 435            | Medium         | 45min     | Greedy by end          |              |
| Done 193     | Minimum Number of Arrows to Burst Balloons     | 452            | Medium         | 45min     | Greedy by end          |              |
| Done 194     | Partition Labels                               | 763            | Medium         | 45min     | Greedy partition       |              |
| Done 195     | Remove K Digits                                | 402            | Medium         | 60min     | Greedy + stack         |              |
| Done 196     | Lemonade Change                                | 860            | Easy           | 30min     | Greedy counts          |              |

**March Add-On Total:** 50 problems (~35.75 hours)

## Current Practice Queue (Apr 2026)

Use this as the **practice-now** set from the questions still open in the plan. It is biased toward high-frequency interview patterns and good topic coverage.

### Design Data Structures (Gap-Fill — added Jul 5)

No "design a data structure" problems exist anywhere in this plan despite heavy drilling on patterns like Jump Game (9 variants) and Stock Buy/Sell (8 variants). This is a real coverage gap — design problems test API design + right-structure-choice, not algorithm pattern-matching, and are near-certain in FAANG loops (esp. Amazon/Google/Meta). Prioritize these over any further stock/jump-game variants.

| #   | Priority     | Problem                          | LeetCode #     | Difficulty     | Time      | Key Concept                                |
|-----|--------------|----------------------------------|----------------|----------------|-----------|--------------------------------------------|
| 197 | P1           | LRU Cache                        | 146            | Medium         | 45min     | Hash map + doubly linked list              |
| 198 | P1           | Insert Delete GetRandom O(1)     | 380            | Medium         | 30min     | Hash map + array swap-remove               |
| 199 | P1           | Design Twitter                   | 355            | Medium         | 45min     | Hash map + heap, OOP API design            |
| 200 | P2           | LFU Cache                        | 460            | Hard           | 60min     | Two hash maps + freq buckets (stretch)     |

### System Design (In Progress)

| #   | Problem                | Status          | Time       | Notes                                                                                                       |
|-----|------------------------|-----------------|------------|-------------------------------------------------------------------------------------------------------------|
| D11 | Facebook Messenger     | In progress     | ~2.5h+     | Use `SYSTEM_DESIGN_TEMPLATE.md` + `FACEBOOK_MESSENGER_EXAMPLE.md`; Steps 1–2 done, continue from Step 3     |

### Priority Set (Start Here)

| #   | Priority     | Problem                             | LeetCode #     | Difficulty     | Why now                                               |
|-----|--------------|-------------------------------------|----------------|----------------|-------------------------------------------------------|
| 154 | P1           | Add Two Numbers                     | 2              | Medium         | Classic linked list carry handling                    |
| 165 | P1           | Kth Largest Element in an Array     | 215            | Medium         | Heap / quickselect staple                             |
| 170 | P1           | Task Scheduler                      | 621            | Medium         | Greedy + heap, very interview-friendly                |
| 171 | P1           | Reorganize String                   | 767            | Medium         | Heap + counting, good pattern crossover               |
| 95  | P1           | Find Eventual Safe States           | 802            | Medium         | Graph reversal / topo intuition                       |
| 190 | P1           | Sum of Two Integers                 | 371            | Medium         | Clean bit-manipulation practice                       |
| 94  | P1           | Critical Connections                | 1192           | Hard           | Tarjan / bridge-finding, very strong graph signal     |
| 107 | Done P1      | Alien Dictionary                    | 269            | Hard           | Topological sort with edge construction               |
| 164 | Done P1      | Largest Rectangle in Histogram      | 84             | Hard           | Monotonic stack must-know                             |
| 183 | Done P1      | Split Array Largest Sum             | 410            | Hard           | Binary search on answer space                         |

### Stretch Set (Next Wave)

| #   | Priority     | Problem                        | LeetCode #     | Difficulty     | Why now                              |
|-----|--------------|--------------------------------|----------------|----------------|--------------------------------------|
| 187 | P2           | Counting Bits                  | 338            | Easy           | Fast bit-DP cleanup                  |
| 188 | P2           | Reverse Bits                   | 190            | Easy           | Good low-cost bit revision           |
| 87  | P2           | Palindrome Partitioning II     | 132            | Hard           | DP string cut optimization           |
| 105 | P2           | Burst Balloons                 | 312            | Hard           | Range DP classic                     |
| 139 | P2           | Reconstruct Itinerary          | 332            | Hard           | Eulerian path pattern                |
| 121 | P2           | Redundant Connection II        | 685            | Hard           | Directed union-find variant          |
| 141 | P2           | Swim in Rising Water           | 778            | Hard           | Dijkstra / union-find comparison     |

### Lower Priority / Only If You Have Time

| #   | Problem                                       | LeetCode #     | Difficulty     | Notes                                                   |
|-----|-----------------------------------------------|----------------|----------------|---------------------------------------------------------|
| 42  | Best Time V (Normal + Short)                  | 3573           | Medium         | Niche variant; lower interview ROI                      |
| 43  | Best Time to But/Sell Stock with Strategy     | 309            | Medium         | Looks like a duplicate/variant entry                    |
| 54  | Sliding Window Median                         | 480            | Hard           | Good problem, but lower ROI than the P1 set             |
| 138 | Word Ladder II                                | 126            | Hard           | Useful, but heavier than the current queue              |
| 172 | IPO                                           | 502            | Hard           | Nice heap problem after Task Scheduler / Reorganize     |
| 106 | Scramble String                               | 87             | Hard           | Valid hard DP practice, but not first-priority          |

## FAANG Readiness Checklist

~~After completing this plan, you should be comfortable with:

**LeetCode:**

| Topic             | Covered                                                             |
|-------------------|---------------------------------------------------------------------|
| Arrays            | Two pointers, sliding window, subarray problems, intervals          |
| DP                | 1D, 2D, LCS, LIS, state machine patterns, string DP                 |
| Graphs            | BFS/DFS, shortest path (Dijkstra), topological sort, union-find     |
| Trees             | Traversals, BST operations, tree construction, tree DP              |
| Backtracking      | Permutations, combinations, subsets, constraint problems            |
| Strings           | Anagram patterns, palindromic subsequences                          |
| Trie              | Basic operations, prefix matching, word search                      |
| Hard Problems     | 49 hard problems across all topics                                  |

---~~
