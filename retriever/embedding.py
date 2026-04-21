#============================ 嵌入式模型（BGE、m3e）============================================
# 一句话：把文字变成计算机能计算的数字向量。
# 负责加载开源嵌入模型（比如 bge-m3）
# 所有 “语义相似度计算” 都靠它
# 给向量库提供向量化能力
# 是整个 RAG 的语义基础
# ===========================================================
# 文本嵌入（Embedding）工具
# 作用：把文本变成向量，用于 语义检索 / 相似度匹配
# 这里使用 BGE-M3 中文最强嵌入模型之一
# ===========================================================

# 导入 OpenAI 兼容嵌入模型（用于智谱 API）
from langchain_openai import OpenAIEmbeddings

# 从配置文件导入模型名称（可自由切换）
from config import ZHIPU_EMBEDDING_MODEL


def get_embedding():
    """
    获取全局通用的文本嵌入模型（向量化工具）
    项目所有向量化操作都用这同一个模型
    :return: 嵌入模型实例
    """
    # 创建并返回智谱 API 嵌入模型（兼容 OpenAI 协议）
    from langchain_openai import OpenAIEmbeddings
    from config import ZHIPU_API_KEY

    return OpenAIEmbeddings(
        model=ZHIPU_EMBEDDING_MODEL,
        openai_api_key=ZHIPU_API_KEY,
        openai_api_base="https://open.bigmodel.cn/api/paas/v4",
    )