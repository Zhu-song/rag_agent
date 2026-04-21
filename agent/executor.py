# ============================= 任务执行器 ===========================
# 类型注解：Dict字典、Any任意类型
from typing import Dict, Any
# 导入工具调度器：负责真正运行工具（计算器、天气、搜索等）
from .mcp.scheduler import MCPScheduler


class AgentExecutor:
    """
    任务执行器：专门负责【调用工具、执行任务】
    接收任务规划器的子任务，调用工具执行，并返回执行结果
    """
    
    # 初始化：传入工具调度器（必须传，否则无法执行工具）
    def __init__(self, scheduler: MCPScheduler):
        # 保存调度器到实例变量，供执行任务时使用
        self.scheduler = scheduler

    def execute_task(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个子任务
        :param tool_name: 要调用的工具名
        :param params: 工具需要的参数
        :return: 执行结果（状态+结果/错误信息）
        """
        
        # 如果没有工具名（tool_name为空/None），表示不需要调用工具
        if not tool_name:
            return {"status": "skipped", "result": ""}

        # 尝试执行工具
        try:
            # 通过调度器运行工具，传入参数
            res = self.scheduler.run_tool(tool_name, **params)
            # 执行成功：返回成功状态 + 结果
            return {"status": "success", "result": res}
        
        # 执行失败（如工具不存在、参数错误、网络异常）
        except Exception as e:
            # 返回失败状态 + 错误原因
            return {"status": "failed", "error": str(e)}