class Solution:
    def medianSlidingWindow(self, nums: list[int], k: int) -> list[float]:

        small = []   # max heap (negative values)
        large = []   # min heap

        delayed = defaultdict(int)

        small_size = 0
        large_size = 0

        def prune_small():
            nonlocal small_size

            while small and delayed[-small[0]]:
                num = -heapq.heappop(small)
                delayed[num] -= 1

        def prune_large():
            nonlocal large_size

            while large and delayed[large[0]]:
                num = heapq.heappop(large)
                delayed[num] -= 1

        def add(num):
            nonlocal small_size, large_size

            if not small or num <= -small[0]:
                heapq.heappush(small, -num)
                small_size += 1
            else:
                heapq.heappush(large, num)
                large_size += 1

            # rebalance
            if small_size > large_size + 1:
                x = -heapq.heappop(small)
                heapq.heappush(large, x)
                small_size -= 1
                large_size += 1

            elif large_size > small_size:
                x = heapq.heappop(large)
                heapq.heappush(small, -x)
                large_size -= 1
                small_size += 1

        def remove(num):
            nonlocal small_size, large_size

            delayed[num] += 1

            if num <= -small[0]:
                small_size -= 1

                if num == -small[0]:
                    prune_small()
            else:
                large_size -= 1

                if large and num == large[0]:
                    prune_large()

            # rebalance
            if small_size > large_size + 1:
                x = -heapq.heappop(small)
                heapq.heappush(large, x)
                small_size -= 1
                large_size += 1

            elif large_size > small_size:
                x = heapq.heappop(large)
                heapq.heappush(small, -x)
                large_size -= 1
                small_size += 1

        def median():
            prune_small()
            prune_large()

            if k % 2:
                return float(-small[0])

            return (-small[0] + large[0]) / 2

        # Build first window
        for i in range(k):
            add(nums[i])

        ans = [median()]

        # Slide
        for i in range(k, len(nums)):
            add(nums[i])
            remove(nums[i - k])

            ans.append(median())

        return ans