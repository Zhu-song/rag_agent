# mcp/tool_registry.py
from typing import List, Dict

class ToolRegistry:
    def __init__(self):
        self.tools = []
        self.func_map = {}  # 工具名 → 执行函数

    def list_tools(self) -> List[Dict]:
        return self.tools