#======================== 基础 RAG Chain ========================
# 无 langchain，无 pydantic，纯手写，绝对不报错
from llm.chat_model import get_chat_llm
from retriever.vector_store import get_faiss_retriever


def get_rag_chain():
    """标准 RAG 问答链（纯手写，无第三方依赖冲突）"""
    llm = get_chat_llm()
    retriever = get_faiss_retriever()

    if not retriever:
        raise Exception("向量库不存在，请先构建知识库！")

    # 手写 RAG 逻辑，不依赖任何 LangChain 组件
    def run_chain(inputs):
        query = inputs["query"]
        
        # 1. 检索文档
        docs = retriever.invoke(query)
        context = "\n".join([d.page_content for d in docs])

        # 2. 拼接提示词
        prompt = f"""
你是专业的文档问答助手。请根据上下文回答问题，遵循以下格式要求：

## 格式要求：
1. 使用 Markdown 格式输出
2. 用 ## 添加小标题分段
3. 用 - 或 1. 2. 3. 列表展示要点
4. 重要内容用 **加粗** 标注
5. 代码或命令用 ``` 包裹
6. 保持回答结构清晰、层次分明

## 回答结构示例：
### 📌 核心结论
简要回答核心问题...

### 📝 详细说明
- 要点一
- 要点二
- 要点三

### 💡 补充信息
相关扩展内容...

---

上下文：
{context}

用户问题：{query}

请按上述格式要求回答：
"""

        # 3. 调用大模型
        response = llm.invoke(prompt)
        
        # 4. 返回结果
        return {
            "result": response.content if hasattr(response, "content") else str(response),
            "source_documents": docs
        }

    return run_chain


def rag_answer(query: str):
    """对外接口：直接获取答案"""
    chain = get_rag_chain()
    result = chain({"query": query})
    return result["result"]