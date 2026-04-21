#===================== 混合检索器（BM25 + 嵌入式模型）============================================
# 一句话：把语义检索 + 关键词检索融合，效果翻倍。
# 向量检索（懂语义）占 60%
# BM25 关键词（精准匹配）占 40%
# 输出一个综合最相关的文档列表
# 工业级 RAG 标配
# ===========================================================
# 混合检索器（RAG 最强标配）
# 原理：向量检索（语义理解） + BM25（关键词匹配）= 效果翻倍
# 权重：向量 60% + BM25 40%（工业界最常用配比）
# ===========================================================

# 导入 LangChain 官方混合检索器（新版正确导入）
from langchain_community.retrievers import EnsembleRetriever

# 导入你自己写的 向量检索器（FAISS）
from .vector_store import get_faiss_retriever

# 导入你自己写的 关键词检索器（BM25）
from .bm25_retriever import get_bm25_retriever

# 从配置文件读取：检索返回的最大条数
from config import RETRIEVE_TOP_K


def get_hybrid_retriever(docs: list[str]):
    """
    创建 RAG 混合检索器
    融合：向量检索（语义） + BM25 检索（关键词）
    :param docs: 分块后的文本列表
    :return: 混合检索器（最终 RAG 使用这个）
    """
    # 1. 获取 FAISS 向量检索器（语义相似度检索）
    faiss_ret = get_faiss_retriever()

    # 2. 获取 BM25 关键词检索器（精确词匹配检索）
    bm25_ret = get_bm25_retriever(docs)

    # 3. 容错机制：如果向量检索器加载失败，只返回 BM25 保证可用
    if not faiss_ret:
        return bm25_ret

    # 4. 创建混合检索器（Ensemble）
    #    retrievers：放入两个检索器
    #    weights：权重分配 [向量, BM25]
    ensemble_retriever = EnsembleRetriever(
        retrievers=[faiss_ret, bm25_ret],
        weights=[0.6, 0.4]
    )

    # 5. 返回最终混合检索器（给 RAG 链使用）
    return ensemble_retriever
