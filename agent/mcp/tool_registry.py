# mcp/tool_registry.py
# Agent模块专用工具注册中心（与 mcp/tool_registry.py 保持一致）
from typing import Callable, Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class ToolInfo:
    """工具元信息：记录一个工具的所有基本信息"""
    name: str
    desc: str
    func: Callable[..., Any]
    params_schema: Dict[str, Any] = field(default_factory=dict)


class ToolRegistry:
    """工具注册中心"""

    def __init__(self):
        # 工具仓库：key=工具名，value=ToolInfo 对象
        self.tools: Dict[str, ToolInfo] = {}
        # 兼容旧代码的 func_map
        self.func_map: Dict[str, Callable] = {}

    def register(
        self,
        name: str,
        desc: str,
        params_schema: Dict[str, Any] = None
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """
        装饰器方法：用于注册工具
        使用方式：@register(name="xxx", desc="xxx")
        """
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.tools[name] = ToolInfo(
                name=name,
                desc=desc,
                func=func,
                params_schema=params_schema or {}
            )
            # 同步更新 func_map，兼容旧代码
            self.func_map[name] = func
            return func
        return decorator

    def get_tool(self, name: str) -> Optional[ToolInfo]:
        """根据工具名称，从仓库中取出对应的工具信息"""
        return self.tools.get(name)

    def list_tools(self) -> List[Dict[str, Any]]:
        """
        获取所有工具的描述信息列表
        主要给 Planner / LLM 使用，让模型知道有哪些工具可用
        """
        return [
            {
                "name": tool.name,
                "desc": tool.desc,
                "params_schema": tool.params_schema
            }
            for tool in self.tools.values()
        ]

    def has_tool(self, name: str) -> bool:
        """判断某个工具是否已经注册"""
        return name in self.tools


# 全局工具注册中心实例
tool_registry = ToolRegistry()
