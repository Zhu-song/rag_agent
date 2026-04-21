#============================= 工具执行器 ===========================================

# MCPToolExecutor = 工具调用入口（门面）

# 它自己不执行工具，只是：
# 包装 MCPScheduler
# 给外部提供更简单、更统一的调用方式
# 让 Agent 不用关心底层调度细节


# mcp/tool_executor.py
# 导入类型提示：字典、任意类型
from typing import Dict, Any

# 从当前目录的 scheduler 导入工具调度器
from .scheduler import MCPScheduler


class MCPToolExecutor:
    """
    工具执行封装类
    作用：对工具调度器 MCPScheduler 做一层简化包装
    让外部调用工具时更简单、更统一
    相当于 Agent 调用工具的“入口”
    """

    def __init__(self):
        """
        初始化：创建工具调度器实例
        """
        # 内部持有一个 MCPScheduler 实例
        self.scheduler = MCPScheduler()

    def invoke(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个工具（对外暴露的接口）
        :param tool_name: 工具名称
        :param params: 参数字典
        :return: 工具执行结果
        """
        # 调用调度器的 run_tool 方法
        return self.scheduler.run_tool(tool_name, **params)

    def invoke_batch(self, tasks: list) -> list:
        """
        批量执行多个工具
        :param tasks: 任务列表
        :return: 批量执行结果
        """
        # 调用调度器的批量执行方法
        return self.scheduler.batch_run(tasks)