class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """3. 无重复字符的最长子串（中等）· 滑动窗口
        题目链接: https://leetcode.cn/problems/longest-substring-without-repeating-characters/
        """
        #无重复最长字串类使用滑动窗口求解
        n = len(s)
        left = 0
        windows = set() 
        result = 0
        for right in range(n) :
            while s[right] in windows :
                windows.discard(s[left]) #集合弹出一个特定元素要用discard ，不能用pop，集合的pop是随机弹出一个，不接受参数
                left += 1
            windows.add(s[right])
            result = max(result,right-left+1)
        return result

         
