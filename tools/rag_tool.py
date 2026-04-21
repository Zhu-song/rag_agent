#============================= RAG 工具 ===========================================
# 导入MCP工具注册中心（用来把RAG功能注册成AI可调用工具）
from mcp.tool_registry import tool_registry

# 导入你自己的RAG链（核心：从本地知识库检索答案）
from chain.rag_chain import get_rag_chain


# ==========================================
# 把 RAG 检索 注册为 MCP 工具
# 这样 Agent / 调度器 都可以调用它
# ==========================================
@tool_registry.register(
    name="rag_retrieval",        # 工具名称（调用时用这个名字）
    desc="从本地知识库检索相关文档回答问题",  # 工具描述（给大模型看，让它知道什么时候用）
    params_schema={"query": "用户问题"}      # 参数说明：需要传入用户问题 query
)
def rag_tool(query: str):
    """
    RAG 工具的真正执行函数
    :param query: 用户的问题/查询语句
    :return: 从本地知识库检索到的答案
    """
    # 调用 RAG 链，查询知识库并返回结果
    rag_chain = get_rag_chain()
    result = rag_chain({"query": query})
    return result["result"]
