# mcp/scheduler.py
from typing import Any

class MCPScheduler:
    def __init__(self, registry):
        self.registry = registry

    def run_tool(self, tool_name: str, **params) -> Any:
        if tool_name not in self.registry.func_map:
            return f"工具 {tool_name} 未注册"
        
        func = self.registry.func_map[tool_name]
        return func(**params)