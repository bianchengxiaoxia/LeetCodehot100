class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        """438. 找到字符串中所有字母异位词（中等）· 滑动窗口
        题目链接: https://leetcode.cn/problems/find-all-anagrams-in-a-string/
        """
        #这个解法可以是可以，但是过多的sort排序增加了时间复杂度
        # p = ''.join(sorted(p))
        # n1= len(s)
        # n2 = len(p)
        # left = 0
        # right = n2
        # result = []
        # while right <= n1 :
        #     if ''.join(sorted(s[left:right])) == p :
        #         result.append(left)
        #     left += 1
        #     right += 1
        # return result

        #标准解法，使用数组来标记字串，将对应位置标为1，这样每次滑动窗口后比较的时间复杂度将为o(1)
        n1 = len(s)
        n2 = len(p)
        if n2 > n1 :
            return []
        win = [0]*26
        need = [0]*26
        result = []
        for ch in p :
            need[ord(ch)-ord('a')] += 1
        for i in range(n1) :
            win[ord(s[i])-ord('a')] +=1
            if i > n2-1 :
                win[ord(s[i-n2])-ord('a')] -= 1
            if i >= n2-1 and win == need :
                result.append(i-n2+1)
        return result


            
