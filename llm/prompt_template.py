#==================== 提示词工程 ==========================
from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage


def get_rag_prompt():
    return PromptTemplate(
        template="""请根据上下文回答问题，不要编造内容。
上下文：
{context}

问题：{question}
回答：""",
        input_variables=["context", "question"]
    )


def get_agent_system_prompt():
    return SystemMessage(
        content="你是一个智能任务助手，可以调用工具：RAG检索、计算器、文件读取、网络搜索。"
    )


def get_chat_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", "根据文档内容回答，简洁准确。"),
        MessagesPlaceholder("chat_history"),
        ("user", "{query}")
    ])
