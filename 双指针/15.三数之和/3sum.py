class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """15. 三数之和（中等）· 双指针
        题目链接: https://leetcode.cn/problems/3sum/
        """
        # 进化史：第一版"固定前两个数 + set 查第三个"——正确性修到对拍全绿，
        # 但每轮 set(切片) 是 O(n)，嵌进双层循环 → O(n³) 必超时（详见《解题思路与收获.md》）
        # 正确轨道：只固定第一个数，后两个数对撞双指针 → O(n²)

        nums.sort()                                # 排序：对撞 + 去重的共同前提
        length = len(nums)
        result = []
        for i in range(length - 2):                # 固定第一个数
            if nums[i] > 0:                        # 剪枝：最小数都>0，后面全正
                break
            if i > 0 and nums[i] == nums[i - 1]:
                # 跳重一：不让同一个值第二次当"第一数"。
                # 第二次的搜索窗口是第一次的真子集，产出的只能是重复解；
                # 重复值本身仍作为原料留在窗口里（[-1,-1,2] 不丢）
                continue
            left = i + 1
            right = length - 1
            while left < right:                    # 对撞找两数之和 = -nums[i]
                s = nums[i] + nums[left] + nums[right]
                if s < 0:
                    left += 1
                elif s > 0:
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    # 找到解后 left/right 各挪一步，再和"刚用过的值"比较跳重
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
        # 注意 return 的缩进：必须和 for 对齐（写在循环外），写进循环里会提前返回
        return result
