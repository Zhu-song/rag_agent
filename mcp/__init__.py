from .scheduler import MCPScheduler
from .tool_executor import MCPToolExecutor
from .tool_registry import ToolRegistry, tool_registry, ToolInfo
from .tool_manager import ToolManager


__all__ = [
    "ToolRegistry",
    "tool_registry",
    "ToolInfo",
    "ToolManager",
    "MCPScheduler",
    "MCPToolExecutor",
]


# 用户提问
#    ↓
# Agent（agent/）思考：我需要用 RAG + 计算器
#    ↓
# Agent 把任务发给 MCP 调度中心（mcp/）
#    ↓
# MCP 去调用具体工具（tools/）
#    ↓
# 工具执行完，结果返回给 MCP → Agent → 最终回答