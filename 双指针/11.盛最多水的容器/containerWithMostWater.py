class Solution:
    def maxArea(self, height: List[int]) -> int:
        """11. 盛最多水的容器（中等）· 双指针
        题目链接: https://leetcode.cn/problems/container-with-most-water/
        """
        #这版比较抽象，不好读，不优雅，可以将计算最大值提取出来，且命名不好
        # slow = 0
        # fast = len(height)-1
        # best = 0
        # while slow < fast :
        #     if height[slow] < height[fast] :
        #         slow += 1
        #         best = max(best,(fast-slow+1)*height[slow-1])
        #     else :
        #         fast -= 1
        #         best = max(best,(fast-slow+1)*height[fast+1])
        # return best

        left = 0
        right = len(height)-1
        best = 0
        while left < right :
            best = max(best ,(right-left)*min(height[left],height[right]))
            if height[left] < height[right]:
                left += 1
            else :
                right -= 1
        return best
            

