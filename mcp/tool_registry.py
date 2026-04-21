#============================== 工具注册中心 ==========================================
# 工具注册表
# mcp/tool_registry.py
# 导入类型提示相关库（用于规范参数、返回值的类型）
from typing import Callable, Dict, Any, Optional, List

# 导入数据类装饰器，用于快速创建只存储数据的类
from dataclasses import dataclass, field


# ------------------------------
# ToolInfo：每个工具的“信息包”
# 用来统一存放：工具名、描述、执行函数、参数格式
# ------------------------------
@dataclass
class ToolInfo:
    """工具元信息：记录一个工具的所有基本信息"""
    # 工具名称（唯一标识，用于调用）
    name: str
    # 工具功能描述（给大模型看，让它知道这个工具干什么用）
    desc: str
    # 真正执行逻辑的 Python 函数
    func: Callable[..., Any]
    # 参数格式定义，默认是空字典
    # default_factory=dict 表示每个实例自动新建一个空 dict
    params_schema: Dict[str, Any] = field(default_factory=dict)


# ------------------------------
# ToolRegistry：全局唯一的工具注册中心
# 作用：统一管理、存储、查询所有 Agent 可调用的工具
# 采用单例模式，整个系统只有一个实例
# ------------------------------
class ToolRegistry:
    """单例工具注册中心"""

    # 类变量：保存唯一的实例，实现单例
    _instance: Optional["ToolRegistry"] = None

    def __new__(cls) -> "ToolRegistry":
        """
        重写 __new__ 实现单例模式
        保证整个程序永远只有一个 ToolRegistry 实例
        """
        # 如果还没有创建实例，就创建一个
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # 执行初始化（只执行一次）
            cls._instance._init()
        # 返回唯一实例
        return cls._instance

    def _init(self) -> None:
        """
        初始化工具仓库
        只在第一次创建实例时调用
        """
        # 工具仓库：key=工具名，value=ToolInfo 对象
        self.tools: Dict[str, ToolInfo] = {}

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
        # 内部装饰器：接收被装饰的函数
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            # 把函数包装成 ToolInfo 并存入工具仓库
            self.tools[name] = ToolInfo(
                name=name,
                desc=desc,
                func=func,
                params_schema=params_schema or {}
            )
            # 返回原函数，不影响函数本身使用
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


# ------------------------------
# 创建全局唯一的工具注册中心实例
# 整个 Agent 系统都用这一个对象
# ------------------------------
tool_registry = ToolRegistry()