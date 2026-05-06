#===================== 多轮对话 ======================
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from llm.chat_model import get_chat_llm
from config import LLM_MAX_TOKENS


# 简化的对话记忆实现
class ConversationBufferMemory:
    """对话缓冲记忆"""
    def __init__(self, memory_key="chat_history", return_messages=True):
        self.memory_key = memory_key
        self.return_messages = return_messages
        self.chat_memory = ChatMessageHistory()
    
    def load_memory_variables(self, inputs):
        return {self.memory_key: self.chat_memory.messages}
    
    def save_context(self, inputs, outputs):
        from langchain_core.messages import HumanMessage, AIMessage
        self.chat_memory.add_message(HumanMessage(content=inputs.get("input", "")))
        self.chat_memory.add_message(AIMessage(content=outputs.get("output", "")))


def get_conversation_memory():
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )


def get_summary_memory():
    """摘要记忆（简化版，使用缓冲记忆代替）"""
    return get_conversation_memory()
