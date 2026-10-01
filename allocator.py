class Allocator:
    def __init__(self, N: int):
        self.memory_size = N
        self.allocated = {}

    def alloc(self, size: int) -> int:
        best_addr = self._find_best_position(size)

        if best_addr != -1:
            self.allocated[best_addr] = size

        return best_addr

    def _find_best_position(self, size: int):
        occupied = set()
        for addr, alloc_size in self.allocated.items():
            for i in range(alloc_size):
                occupied.add(addr + i)

        free_ranges = self._find_free_ranges(occupied)

        # Strategy for best placement:
        # 1. Prefer exact fit (range size == size needed)
        # 2. Then prefer aligned positions in small ranges
        # 3. Then aligned positions in any range
        # 4. Finally any position that fits

        candidates = []

        for start, length in free_ranges:
            if length < size:
                continue

            # Check aligned position
            aligned_start = self._next_aligned(start, size)
            if aligned_start + size <= start + length:
                waste = length - size
                # Prefer aligned and exact/small waste
                candidates.append((waste, 0, aligned_start))

            # Check start position (unaligned)
            if start + size <= start + length:
                waste = length - size
                # Unaligned is secondary choice
                candidates.append((waste, 1, start))

        if not candidates:
            return -1

        # Sort by waste (prefer exact fit), then by alignment preference
        candidates.sort()
        return candidates[0][2]

    def _next_aligned(self, addr, size):
        if addr % size == 0:
            return addr
        return addr + (size - addr % size)

    def _find_free_ranges(self, occupied):
        ranges = []
        start = None

        for addr in range(self.memory_size):
            if addr not in occupied:
                if start is None:
                    start = addr
            else:
                if start is not None:
                    ranges.append((start, addr - start))
                    start = None

        if start is not None:
            ranges.append((start, self.memory_size - start))

        return ranges

    def free(self, address: int) -> None:
        del self.allocated[address]
