#===================== 多轮对话 ======================
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from llm.chat_model import get_chat_llm
from config import LLM_MAX_TOKENS


def get_conversation_memory():
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )


def get_summary_memory():
    llm = get_chat_llm()
    return ConversationSummaryMemory(
        llm=llm,
        memory_key="chat_history",
        return_messages=True
    )
