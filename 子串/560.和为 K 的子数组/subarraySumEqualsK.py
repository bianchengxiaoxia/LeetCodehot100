class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        """560. 和为 K 的子数组（中等）· 子串
        题目链接: https://leetcode.cn/problems/subarray-sum-equals-k/
        """
        # —— 第一版：前缀和 + 双重循环枚举所有 (i, j) ——
        # 思路正确但 O(n²)：n=2万时实测 10 秒+，必超时。留作对照。
        # 下标约定：presum[i] = 前 i 个数的和（长 n+1，presum[0]=0 哨兵），
        # 所以填表配的是 nums[i-1]——"长度 n+1"和"下标减一"形影不离
        # n = len(nums)
        # presum = [0]*(n+1)
        # result = 0
        # for i in range(1, n+1):
        #     presum[i] = presum[i-1] + nums[i-1]
        # for i in range(n):
        #     for j in range(i+1, n+1):
        #         if presum[j] - presum[i] == k:   # 子数组 nums[i..j-1] 的和
        #             result += 1
        # return result

        # —— 标准版：前缀和 + 哈希（两数之和的内核回归）——
        # 核心：子数组和 = 两个前缀和之差。
        # 要 s_new - s_old == k  ⇔  s_old == s_new - k
        # 于是内层"扫所有旧前缀"降级为字典 O(1) 查询：问"比我小 k 的旧前缀有几个"
        count = {0: 1}     # 哨兵：前缀和 0 预登记一次（空前缀），
                           # 覆盖"子数组从下标 0 开始"的情况（此时 s - k == 0）
        result = 0
        s = 0              # 滚动维护当前前缀和，不必真建 presum 数组
        for i in range(len(nums)):
            s += nums[i]
            result += count.get(s - k, 0)   # 先查询：以 i 结尾、和为 k 的子数组有几个
            count[s] = count.get(s, 0) + 1  # 后登记：k=0 时才不会把自己配给自己
        return result
