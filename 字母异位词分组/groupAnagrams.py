class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """49. 字母异位词分组（中等）· 哈希
        题目链接: https://leetcode.cn/problems/group-anagrams/
        """
        group = {}
        for word in strs:
            cnt = [0] * 26
            for ch in word:
                cnt[ord(ch) - ord('a')] += 1
            key = tuple(cnt)
            group.setdefault(key, []).append(word)
        return list(group.values())
