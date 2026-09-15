# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        """105. 从前序与中序遍历序列构造二叉树（中等）· 二叉树
        题目链接: https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
        """
        
