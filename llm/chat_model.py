from langchain_openai import ChatOpenAI
from config import LLM_CONFIG

def get_chat_llm():
    """
    获取大模型实例（智谱 GLM 专用）
    兼容 OpenAI 协议，直接对接 config + .env
    """
    llm = ChatOpenAI(
        api_key=LLM_CONFIG["api_key"],
        base_url=LLM_CONFIG["base_url"],
        model=LLM_CONFIG["model_name"],
        temperature=LLM_CONFIG["temperature"],
        max_tokens=LLM_CONFIG["max_tokens"],
        timeout=LLM_CONFIG["timeout"],
    )
    return llm

# 测试函数
if __name__ == "__main__":
    llm = get_chat_llm()
    response = llm.invoke("你好")
    print(response.content)