treeNode 定义

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val       # 节点的值
        self.left = left     # 左子节点
        self.right = right   # 右子节点


1.确定递归函数的参数和返回值
2.确定终止条件
3.确定单层递归的逻辑