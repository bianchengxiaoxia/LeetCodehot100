class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}  #这是python中的字典  键值对
        for i ,x in enumerate(nums):
            if target - x in seen :
                return [seen[target - x],i]
            seen[x] = i
        return []

 




                    
