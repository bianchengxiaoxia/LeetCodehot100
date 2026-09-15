class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        #个人想法，快慢指针，非标准通用解法，下面写标准通用解法
        # head  = 0
        # end = 1
        # length = len(nums)
        # while end < length :
        #     if nums[head] == 0 :
        #         while end < length and nums[end] == 0:
        #             end += 1
        #         if end <length :
        #             nums[head] =nums[end]
        #             nums[end]  = 0
        #     head += 1
        #     end  += 1
        
        #标准的快慢指针，是数组原地整理的万能模板
        slow = 0 
        for fast in range(len(nums)):
            if nums[fast] != 0:
                nums[slow],nums[fast] = nums[fast],nums[slow]
                slow += 1
            
        
                
                
                
