#============================ 工具管理器 ============================================

# ToolManager = 工具的开关管理员

# 它只干 3 件事：
# 禁用工具
# 启用工具
# 检查工具能不能用



# mcp/tool_manager.py
# 导入类型提示：字典、任意类型
from typing import Dict, Any

# 导入全局工具注册中心（用来检查工具是否存在）
from .tool_registry import tool_registry


class ToolManager:
    """
    工具管理器
    作用：管理工具的【启用 / 禁用】、检查工具是否可以使用
    不负责执行，只负责“能不能用”
    """

    def __init__(self):
        """
        初始化：创建一个集合，用来存放【被禁用的工具名】
        set 集合特点：自动去重、查找超快
        """
        self.disabled_tools = set()

    def disable(self, tool_name: str):
        """
        禁用某个工具
        :param tool_name: 工具名称
        """
        self.disabled_tools.add(tool_name)

    def enable(self, tool_name: str):
        """
        启用某个工具（解除禁用）
        :param tool_name: 工具名称
        """
        # discard：不存在也不会报错，比 remove 更安全
        self.disabled_tools.discard(tool_name)

    def is_available(self, tool_name: str) -> bool:
        """
        检查一个工具【是否可以正常使用】
        :param tool_name: 工具名
        :return: 可用返回 True，不可用返回 False
        """
        # 1. 先检查工具是否在注册中心里存在
        if not tool_registry.has_tool(tool_name):
            return False

        # 2. 再检查工具是否被禁用
        # 没被禁用 → 可用
        return tool_name not in self.disabled_tools