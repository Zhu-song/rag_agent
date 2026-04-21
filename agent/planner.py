# ========================== 任务规划器 ==========================
# 类型注解：List列表、Dict字典、Any任意类型
from typing import List, Dict, Any
# 导入大模型获取方法，用于AI思考规划
from .llm.chat_model import get_chat_llm
# 处理JSON格式，解析AI返回的任务列表
import json


class TaskPlanner:
    """
    任务规划器：把用户复杂问题 → 拆成多个有序子任务
    作用：让AI先把大问题拆小，再交给智能体一步步执行
    """
    def __init__(self):
        # 初始化大语言模型（AI大脑）
        self.llm = get_chat_llm()

    def plan(self, query: str, tools: List[Dict]) -> List[Dict]:
        """
        核心方法：问题拆分 + 任务规划
        :param query: 用户问题
        :param tools: 可用工具列表（告诉AI能使用哪些工具）
        :return: 子任务列表（有序数组）
        """
        # 把工具列表转成文字描述，让AI能看懂
        tool_str = "\n".join([f"- {t['name']}: {t['desc']}" for t in tools])

        # 构造提示词：严格要求AI输出【子任务JSON数组】
        prompt = f"""
你是任务规划器，请把用户问题拆分为 1~3 个有序子任务。
可用工具：
{tool_str}

输出严格 JSON 数组，不要其他内容：
[
    {{
        "task": "任务描述",
        "tool": "工具名",
        "params": {{}}
    }}
]

用户问题：{query}
"""

        # 调用大模型生成子任务，去除多余空格换行
        resp = self.llm.invoke(prompt).content.strip()

        # 尝试解析JSON，返回子任务列表
        try:
            return json.loads(resp)
        # 解析失败 → 返回默认任务：直接回答
        except json.JSONDecodeError:
            return [{"task": "直接回答", "tool": None, "params": {}}]