class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        """128. 最长连续序列（中等）· 哈希
        题目链接: https://leetcode.cn/problems/longest-consecutive-sequence/
        """
        s = set(nums) 
        best = 0
        for x in s:
            if x-1 not in s:
                length = 1
                while x+1 in s:
                    length += 1
                    x += 1
                best = max(length,best)
        return best
