class Solution:
    def maximumProfit(self, prices: List[int], k: int) -> int:

        n = len(prices)

        buy = [-prices[0]] * (k + 1)
        short = [prices[0]] * (k + 1)
        curr = [0] * (k + 1)

        for i in range(n):
            prev_buy = buy.copy()
            prev_short = short.copy()
            prev_curr = curr.copy()

            for j in range(1, k + 1):
                buy[j] = max(buy[j], prev_curr[j - 1] - prices[i])
                short[j] = max(short[j], prev_curr[j - 1] + prices[i])
                curr[j] = max(prev_curr[j], prev_buy[j] - prices[i], prev_short[j] + prices[i])

        return curr[-1]