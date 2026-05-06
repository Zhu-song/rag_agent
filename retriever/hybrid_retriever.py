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

from typing import List
from langchain_core.documents import Document

# 导入你自己写的 向量检索器（FAISS）
from .vector_store import get_faiss_retriever

# 导入你自己写的 关键词检索器（BM25）
from .bm25_retriever import get_bm25_retriever

# 从配置文件读取：检索返回的最大条数
from config import RETRIEVE_TOP_K


class HybridRetriever:
    """
    混合检索器：融合向量检索 + BM25 检索
    """
    def __init__(self, vector_retriever, bm25_retriever, vector_weight=0.6, top_k=6):
        self.vector_retriever = vector_retriever
        self.bm25_retriever = bm25_retriever
        self.vector_weight = vector_weight
        self.bm25_weight = 1 - vector_weight
        self.top_k = top_k
    
    def invoke(self, query: str) -> List[Document]:
        """执行混合检索"""
        results = []
        
        # 1. 向量检索
        if self.vector_retriever:
            try:
                vector_docs = self.vector_retriever.invoke(query)
                for i, doc in enumerate(vector_docs[:self.top_k]):
                    doc.metadata["vector_score"] = 1.0 / (i + 1)  # 倒数排名作为分数
                    doc.metadata["source"] = "vector"
                    results.append(doc)
            except Exception as e:
                print(f"向量检索失败: {e}")
        
        # 2. BM25 检索
        if self.bm25_retriever:
            try:
                bm25_docs = self.bm25_retriever.invoke(query)
                for i, doc in enumerate(bm25_docs[:self.top_k]):
                    doc.metadata["bm25_score"] = 1.0 / (i + 1)
                    doc.metadata["source"] = "bm25"
                    results.append(doc)
            except Exception as e:
                print(f"BM25检索失败: {e}")
        
        # 3. 合并去重（按内容去重）
        seen = set()
        unique_results = []
        for doc in results:
            content_hash = hash(doc.page_content[:100])  # 取前100字符做hash
            if content_hash not in seen:
                seen.add(content_hash)
                unique_results.append(doc)
        
        # 4. 计算综合分数并排序
        for doc in unique_results:
            vector_score = doc.metadata.get("vector_score", 0)
            bm25_score = doc.metadata.get("bm25_score", 0)
            doc.metadata["final_score"] = vector_score * self.vector_weight + bm25_score * self.bm25_weight
        
        # 5. 按综合分数排序，返回 top_k
        unique_results.sort(key=lambda x: x.metadata.get("final_score", 0), reverse=True)
        return unique_results[:self.top_k]


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

    # 4. 创建混合检索器
    return HybridRetriever(
        vector_retriever=faiss_ret,
        bm25_retriever=bm25_ret,
        vector_weight=0.6,
        top_k=RETRIEVE_TOP_K
    )
