#============================= 关键词检索 ===========================================
# 一句话：靠关键词匹配找文档，类似传统搜索引擎。
# 不看语义，只看 "词有没有出现、出现多少次"
# 擅长：精确词匹配、专业术语、实体名称
# 弥补向量检索 "关键词不敏感" 的缺点
# ===========================================================
# BM25 关键词检索器
# 作用：基于关键词匹配的传统检索方式，专门做"精确关键词搜索"
# 常用于 RAG 混合检索 = BM25(关键词) + 向量检索(语义)
# ===========================================================

# 导入 BM25 检索器（新版 LangChain 正确路径）
from langchain_community.retrievers import BM25Retriever

# 导入文档结构：用来把文本包装成 LangChain 标准的 Document 格式
from langchain_core.documents import Document

# 从配置文件导入：检索召回数量（返回最相似的 topK 条）
from config import RETRIEVE_TOP_K


def get_bm25_retriever(docs: list[str]):
    """
    创建 BM25 关键词检索器
    :param docs: 文本分块后的列表（例如 ["文本1", "文本2"]）
    :return: 可直接使用的 BM25 检索器
    """
    # 1. 把原始字符串列表 包装成 LangChain 需要的 Document 对象列表
    documents = [Document(page_content=d) for d in docs]

    # 2. 从 Document 文档列表中构建 BM25 检索器（自动建立关键词索引）
    retriever = BM25Retriever.from_documents(documents, k=RETRIEVE_TOP_K)

    # 3. 返回构建好的检索器
    return retriever
