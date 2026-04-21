#============================= 工具调度器 ===========================================


# MCPScheduler = 工具执行器

# 它只干三件事：
# 根据工具名找到函数
# 运行工具函数
# 返回统一格式的结果（成功 / 失败）


# mcp/scheduler.py
# 导入类型提示：字典、任意类型
from typing import Dict, Any

# 从当前目录的 tool_registry 导入工具注册中心
from .tool_registry import ToolRegistry, tool_registry

# 从配置文件导入工具执行超时时间
from .config import MCP_TOOL_TIMEOUT


class MCPScheduler:
    """
    MCP 工具调度中心
    作用：根据工具名称，调用对应的函数，并处理成功/失败结果
    相当于 AI Agent 的「工具执行器」
    """

    def __init__(self, registry: ToolRegistry = None):
        """
        初始化调度器
        :param registry: 工具注册中心（不传则使用全局单例）
        """
        # 如果传入了 registry 就用传入的，否则用全局默认的 tool_registry
        self.registry = registry or tool_registry

        # 工具执行超时时间（从 config 读取）
        self.timeout = MCP_TOOL_TIMEOUT

    def run_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        执行单个工具（最核心方法）
        :param tool_name: 工具名称
        :param kwargs: 工具需要的参数（如 a=1, b=2）
        :return: 执行结果（成功/失败）
        """
        # 1. 根据工具名从注册中心查找工具
        tool = self.registry.get_tool(tool_name)

        # 2. 如果工具不存在，直接返回错误
        if not tool:
            return {"error": f"工具不存在：{tool_name}"}

        try:
            # 3. 工具存在 → 调用工具函数，传入参数
            result = tool.func(**kwargs)

            # 4. 返回成功结果（标准格式）
            return {
                "tool": tool_name,
                "status": "success",
                "result": result
            }

        except Exception as e:
            # 5. 执行出错 → 返回失败信息
            return {
                "tool": tool_name,
                "status": "failed",
                "error": str(e)
            }

    def batch_run(self, tasks: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
        """
        批量执行多个工具（简易串行版本）
        :param tasks: 任务列表，格式：[{"tool":"xxx", "params":{"a":1}}]
        :return: 所有工具的执行结果
        """
        results = []

        # 遍历每个任务，依次执行
        for task in tasks:
            # 运行工具，传入参数
            res = self.run_tool(task["tool"], **task.get("params", {}))
            results.append(res)

        # 返回所有结果
        return results