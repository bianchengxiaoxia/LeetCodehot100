from collections import deque


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        """239. 滑动窗口最大值（困难）· 子串
        题目链接: https://leetcode.cn/problems/sliding-window-maximum/
        """
        #本题使用双端队列，队列中存储下标而非值，这样可以方便的查看是否超出窗口大小范围
        
        result = []
        q = deque()
        for i in range(len(nums)):
            while q and nums[i] > nums[q[-1]] : #比较最新一个元素与之前的元素大小，确保队首总是最大值
                q.pop()
            q.append(i)
            if q[0] <= i-k: #最大值的下标移除窗口范围就从左边弹出
                q.popleft()
            if i >= k-1 : #大小达到窗口大小后就可以开始向结果中加入最大值序列
                result.append(nums[q[0]])

        return result
            
