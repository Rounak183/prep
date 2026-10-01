# Revision Notes - kSum Template

## Generic kSum Template

```python
def kSum(nums, target, k):
    """
    Time: O(n^(k-1))
    Space: O(k) for recursion stack
    """
    nums.sort()
    result = []

    def helper(start, target, k, path):
        if k == 2:
            # Two pointers
            left, right = start, len(nums) - 1
            while left < right:
                s = nums[left] + nums[right]
                if s < target:
                    left += 1
                elif s > target:
                    right -= 1
                else:
                    result.append(path + [nums[left], nums[right]])
                    left += 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
            return

        for i in range(start, len(nums) - k + 1):
            # Skip duplicates
            if i > start and nums[i] == nums[i - 1]:
                continue
            # Early termination
            if nums[i] * k > target:
                break
            helper(i + 1, target - nums[i], k - 1, path + [nums[i]])

    helper(0, target, k, [])
    return result
```

## Complexity Table

| Problem | k | Time | Space |
|---------|---|------|-------|
| 2Sum (Hash) | 2 | O(n) | O(n) |
| 2Sum (Two Pointers) | 2 | O(n log n) | O(1) |
| 3Sum | 3 | O(n²) | O(1) |
| 4Sum | 4 | O(n³) | O(1) |
| kSum | k | O(n^(k-1)) | O(k) |

## Key Points

1. **Sort first** (except 2Sum hash approach)
2. **Skip duplicates**: `if i > start and nums[i] == nums[i-1]: continue`
3. **Early termination**: `if nums[i] * k > target: break`
4. **Two pointers** for base case (k=2)

## 2Sum (Hash Map - Most Efficient)

```python
def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

## 3Sum Example

```python
def threeSum(nums):
    nums.sort()
    result = []
    n = len(nums)

    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        if nums[i] > 0:
            break

        left, right = i + 1, n - 1
        target = -nums[i]

        while left < right:
            s = nums[left] + nums[right]
            if s < target:
                left += 1
            elif s > target:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1

    return result
```
