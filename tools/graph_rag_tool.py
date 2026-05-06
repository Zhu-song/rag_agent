#============================== GraphRAG 工具 ==========================================
# 导入 MCP 工具注册中心，用于把当前函数注册成可调用工具
from mcp.tool_registry import tool_registry

# 导入 GraphRAG 知识图谱问答管线
from graph_rag.kgqa_pipeline import KGQAPipeline

# 导入向量 RAG 问答函数（作为降级方案）
from chain.rag_chain import rag_answer


# 全局 KGQA 实例（避免重复创建）
_kgqa_instance = None


def _get_kgqa():
    """获取全局 KGQA 实例（懒加载）"""
    global _kgqa_instance
    if _kgqa_instance is None:
        _kgqa_instance = KGQAPipeline()
    return _kgqa_instance


# 注册工具：将 GraphRAG 注册为 MCP 工具
@tool_registry.register(
    name="graph_rag",                    # 工具名称：Agent 调用时使用
    desc="知识图谱问答，支持实体关系推理查询",  # 工具描述：给大模型看
    params_schema={                     # 参数说明
        "query": "用户问题"
    }
)
def graph_rag_tool(query: str):
    """
    GraphRAG 知识图谱问答工具
    功能：通过知识图谱进行实体关系推理，自动路由到图谱查询或向量检索
    :param query: 用户的问题
    :return: 知识图谱/向量检索的回答结果
    """
    kgqa = _get_kgqa()
    return kgqa.ask(query, vector_rag_func=rag_answer)
