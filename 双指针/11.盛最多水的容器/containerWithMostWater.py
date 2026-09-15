class Solution:
    def maxArea(self, height: List[int]) -> int:
        """11. 盛最多水的容器（中等）· 双指针
        题目链接: https://leetcode.cn/problems/container-with-most-water/
        """
        left, right = 0, len(height) - 1
        best = 0
        while left < right:
            # ① 先记录当前对的面积：宽度 × 短板（木桶效应）
            best = max(best, (right - left) * min(height[left], height[right]))
            # ② 短板在哪边扔哪边：它已配过最宽的对子，弃之不亏
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return best
