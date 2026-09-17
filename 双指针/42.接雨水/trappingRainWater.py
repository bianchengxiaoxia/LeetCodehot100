class Solution:
    def trap(self, height: List[int]) -> int:
        """42. 接雨水（困难）· 双指针
        题目链接: https://leetcode.cn/problems/trapping-rain-water/
        """
        #使用最大前缀和和最大后缀和
        #算我左右最高的元素，这个可以计算出我所在位置的最高水位
        #减去我的高度，即可的我的高度
        n = len(height)
        left_max = [0] * n
        right_max = [0] *n 
        left_max[0] = height[0]
        for i in range(1,n):
            left_max[i] = max(height[i],left_max[i-1])
        right_max[n-1] = height[n-1]
        for i in range(n-2,-1,-1):
            right_max[i] = max(height[i],right_max[i+1])
        
        return sum(min(left_max[i],right_max[i])-height[i] for i in range(n))
        



