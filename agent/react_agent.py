# ========================== 智能体基类 =========================
from typing import Dict, Any
from .base_agent import BaseAgent
from .llm.chat_model import get_chat_llm
from .mcp.scheduler import MCPScheduler
from .mcp.tool_registry import ToolRegistry
import json

# 定义 ReActAgent 智能体类，继承自 BaseAgent（ReAct = 思考+行动+观察 模式）
class ReActAgent(BaseAgent):
    # 初始化方法：创建智能体时自动执行
    def __init__(self):
        # 调用父类 BaseAgent 的初始化方法
        super().__init__()
        # 初始化大语言模型（AI大脑），用于思考、回答问题
        self.llm = get_chat_llm()
        # 初始化工具注册表：存储所有可用工具（计算器、天气、搜索...）
        self.registry = ToolRegistry()
        # 初始化工具调度器：传入工具注册表，负责调用执行工具
        self.scheduler = MCPScheduler(self.registry)

    # 核心方法1：think 思考
    # 功能：接收用户问题 → 让AI分析 → 决定是否调用工具/调用哪个工具
    # 输入：用户问题 query；输出：思考结果（字典格式）
    def think(self, query: str) -> Dict[str, Any]:
        # 从工具注册表中获取所有可用工具列表
        tools = self.registry.list_tools()
        # 把工具列表转换成文字描述（例：- weather: 查询天气 - calculator: 计算器）
        tool_desc = "\n".join([f"- {t['name']}: {t['desc']}" for t in tools])

        # 构造给AI的提示词：严格要求AI按指定JSON格式输出思考结果
        prompt = f"""
你是一个智能任务规划 Agent，请根据用户问题判断使用哪些工具。
可用工具：
{tool_desc}

输出严格 JSON 格式，不要其他任何文字：
{{
    "thought": "分析思路",
    "tool_name": "工具名，无则 null",
    "tool_params": {{参数字典}},
    "need_continue": true/false
}}

用户问题：{query}
"""
        # 调用大模型，传入提示词，获取AI返回的结果，并去除首尾空格
        resp = self.llm.invoke(prompt).content.strip()
        
        # 尝试把AI返回的JSON字符串 转成 Python字典
        try:
            return json.loads(resp)
        # 如果JSON解析失败（AI输出格式错误），返回默认错误结果
        except json.JSONDecodeError:
            return {"thought": "解析失败", "tool_name": None, "tool_params": {}, "need_continue": False}

    # 核心方法2：act 行动
    # 功能：根据思考结果，执行工具 或 直接回答问题
    # 输入：think方法返回的思考结果；输出：执行结果（字典）
    def act(self, thought: Dict[str, Any]) -> Dict[str, Any]:
        # 从思考结果中取出 要调用的工具名
        tool_name = thought.get("tool_name")
        # 从思考结果中取出 工具参数（没有参数则为空字典）
        params = thought.get("tool_params", {})

        # 如果没有指定工具名 → 不需要调用工具，直接让AI回答问题
        if not tool_name:
            return {
                "is_final": True,  # 标记为：最终答案
                "answer": self.llm.invoke(thought["thought"]).content  # AI直接生成答案
            }

        # 如果有工具名 → 使用调度器执行对应工具，传入参数
        result = self.scheduler.run_tool(tool_name, **params)
        # 返回工具执行结果
        # is_final：是否为最终答案（need_continue为false则结束）
        return {
            "is_final": not thought.get("need_continue", True),
            "tool_result": result  # 工具执行的具体结果
        }

    # 核心方法3：observe 观察
    # 功能：把工具执行结果转换成文字，供下一轮思考使用
    # 输入：act方法返回的行动结果；输出：文字描述的结果
    def observe(self, action_result: Dict[str, Any]) -> str:
        # 取出工具结果，转成字符串返回，没有结果则返回"无结果"
        return str(action_result.get("tool_result", "无结果"))
