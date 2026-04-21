# ========================== 智能体基类 ==========================
# ABC：抽象基类，用于定义必须实现的方法
# abstractmethod：抽象方法装饰器，子类必须重写实现
from abc import ABC, abstractmethod
# 类型注解：Dict字典, Any任意类型, Optional可选值（可以为None）
from typing import Dict, Any, Optional
# 时间工具，用于计算超时、记录耗时
import time
# 从配置文件读取：最大迭代次数、思考超时时间
from .config import AGENT_MAX_ITERATIONS, AGENT_THINKING_TIMEOUT


class BaseAgent(ABC):
    """
    Agent 基类（抽象类）
    所有智能体（如ReActAgent）都必须继承此类，统一接口和运行流程
    作用：规定智能体必须有 think、act、observe 方法，并提供统一的 run 运行逻辑
    """

    def __init__(self):
        """初始化智能体基础属性"""
        # 最大思考迭代次数（防止无限循环）
        self.max_iterations = AGENT_MAX_ITERATIONS
        # 单轮思考超时时间（防止卡住太久）
        self.timeout = AGENT_THINKING_TIMEOUT
        # 历史记录：保存每一轮的思考、行动、观察日志
        self.history = []
        # 当前迭代轮数（从0开始计数）
        self.current_iteration = 0

    def reset(self):
        """重置智能体状态"""
        # 清空历史记录
        self.history = []
        # 重置迭代次数
        self.current_iteration = 0

    @abstractmethod
    def think(self, query: str) -> Dict[str, Any]:
        """
        【抽象方法】子类必须实现！
        思考：根据用户问题分析，决定是否调用工具、调用哪个工具
        返回：思考结果字典（思路、工具名、参数等）
        """
        pass

    @abstractmethod
    def act(self, thought: Dict[str, Any]) -> Dict[str, Any]:
        """
        【抽象方法】子类必须实现！
        执行：根据思考结果，执行工具调用 或 直接回答
        返回：执行结果（是否最终答案、工具结果/回答内容）
        """
        pass

    @abstractmethod
    def observe(self, action_result: Dict[str, Any]) -> str:
        """
        【抽象方法】子类必须实现！
        观察：把工具执行结果整理成文字，给下一轮思考使用
        返回：文字描述的观察结果
        """
        pass

    def should_continue(self) -> bool:
        """
        判断是否继续循环迭代
        返回 True：继续思考 → 行动 → 观察
        返回 False：停止循环，给出最终答案
        """
        # 如果当前迭代次数 >= 最大次数 → 停止
        if self.current_iteration >= self.max_iterations:
            return False
        # 否则继续
        return True

    def run(self, query: str) -> Dict[str, Any]:
        """
        【核心主流程】所有智能体统一运行逻辑！
        标准 ReAct 流程：
        思考(think) → 执行(act) → 观察(observe) → 循环 → 结束
        """
        # 运行前先重置状态
        self.reset()
        # 最终答案
        final_answer = ""

        # 循环：只要没达到最大次数，就一直执行
        while self.should_continue():
            # 记录本轮开始时间
            start = time.time()

            # ===================== 1. 思考 =====================
            thought = self.think(query)
            # 把思考结果存入历史日志
            self.history.append({"type": "think", "data": thought})

            # ===================== 2. 执行 =====================
            action_result = self.act(thought)
            # 把执行结果存入历史日志
            self.history.append({"type": "act", "data": action_result})

            # ===================== 3. 观察 =====================
            observation = self.observe(action_result)
            # 把观察结果存入历史日志
            self.history.append({"type": "observe", "data": observation})

            # ===================== 4. 判断是否结束 =====================
            # 如果 act 返回 is_final=True → 已经是最终答案，退出循环
            if action_result.get("is_final", False):
                final_answer = action_result.get("answer", "")
                break

            # 迭代次数 +1
            self.current_iteration += 1

            # 如果单轮耗时超过超时时间 → 强制结束
            if time.time() - start > self.timeout:
                break

        # 返回完整结果：问题、答案、迭代次数、历史日志
        return {
            "query": query,
            "answer": final_answer,
            "iterations": self.current_iteration,
            "history": self.history
        }