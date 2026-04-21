#==================== 向量数据库（FAISS/Chroma）============================================
# 一句话：把向量存起来，并支持快速语义检索。
# 管理 FAISS 本地向量库
# 提供：保存库、加载库、创建检索器
# 你上传文档 → 向量化 → 存在这里
# 提问时，从这里找最相似的内容
# ===========================================================
# FAISS 向量库管理模块
# 功能：本地向量库创建、保存、加载、检索器生成
# ===========================================================

# 导入 FAISS 向量库（轻量级、本地、无需数据库服务）
from langchain_community.vectorstores import FAISS
# 导入嵌入模型（把文本变成向量）
from .embedding import get_embedding
# 导入配置：向量库保存路径、检索数量
from config import VECTOR_DB_DIR, RETRIEVE_TOP_K
# 可选类型注解，让代码更规范
from typing import Optional


def get_vector_store() -> Optional[FAISS]:
    """
    获取 FAISS 向量库实例
    逻辑：如果本地已经存在向量库 → 加载
          如果不存在 → 返回 None
    :return: FAISS 实例 或 None
    """
    # 1. 获取嵌入模型（向量化工具）
    embedding = get_embedding()

    # 2. 判断向量库文件夹是否存在且不为空
    if VECTOR_DB_DIR.exists() and any(VECTOR_DB_DIR.iterdir()):
        # 3. 从本地加载已保存的向量库
        return FAISS.load_local(
            folder_path=str(VECTOR_DB_DIR),       # 向量库路径
            embeddings=embedding,                 # 嵌入模型
            allow_dangerous_deserialization=True  # 允许加载本地文件（必须加）
        )
    # 4. 无向量库时返回 None
    return None


def save_vector_store(documents: list):
    """
    将分块后的文档 向量化 → 保存到本地 FAISS 库
    :param documents: 文本分块后的列表（支持字符串列表或 Document 对象列表）
    :return: FAISS 向量库实例
    """
    # 1. 获取嵌入模型
    embedding = get_embedding()
    # 2. 用文本 + 模型创建向量库（自动判断是字符串列表还是 Document 列表）
    if documents and hasattr(documents[0], 'page_content'):
        db = FAISS.from_documents(documents, embedding)
    else:
        db = FAISS.from_texts(documents, embedding)
    # 3. 保存到本地文件夹
    db.save_local(str(VECTOR_DB_DIR))
    # 4. 返回创建好的库
    return db


def get_faiss_retriever():
    """
    快速获取 FAISS 检索器（给 RAG 调用）
    :return: 检索器 或 None（无向量库时）
    """
    # 1. 获取向量库
    db = get_vector_store()
    # 2. 无库则返回空
    if not db:
        return None
    # 3. 把向量库转为检索器，设置返回 top-K 条最相关结果
    return db.as_retriever(search_kwargs={"k": RETRIEVE_TOP_K})