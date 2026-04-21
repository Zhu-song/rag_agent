#============================================= 父级分块器===================================
# 导入类型提示工具，用于规范函数返回值和参数类型
from typing import List, Dict

# 导入 LangChain 递归文本分割器（最通用、最稳定的文本切分工具）
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 从项目配置文件导入：分块大小、分块重叠长度（统一管理参数）
from .config import CHUNK_SIZE, CHUNK_OVERLAP


def parent_child_split(
    text: str,                        # 输入：需要切分的原始长文本
    parent_chunk_size: int = 1024,    # 父块大小（大段落，保证语义完整）
    child_chunk_size: int = 256,      # 子块大小（小片段，用于精准检索）
    chunk_overlap: int = 50           # 块之间的重叠长度（防止语义断开）
) -> List[Dict]:                      # 输出：包含父子块结构的列表

    """
    父块-子块 双层分块函数（RAG 高级检索核心）
    逻辑：先切大段（父块）→ 再把大段切成小块（子块）
    作用：子块负责检索，父块负责给大模型提供完整上下文
    """

    # ====================== 第一步：创建【父块切分器】 ======================
    # 初始化切分器，用于生成大的父块
    parent_splitter = RecursiveCharacterTextSplitter(

        # 设置父块的最大长度
        chunk_size=parent_chunk_size,

        # 设置父块之间的重叠长度
        chunk_overlap=chunk_overlap,

        # 切割规则：优先按段落、换行、中文句子切割，保证语义完整
        separators=["\n\n", "\n", "。", "！", "？", " "],

        # 长度计算方式：直接按字符数量计算（中英文通用）
        length_function=len
    )

    # 使用父块切分器，将长文本切成多个大父块
    parent_chunks = parent_splitter.split_text(text)

    # ====================== 第二步：创建【子块切分器】 ======================
    # 初始化切分器，用于把父块切成更小的子块
    child_splitter = RecursiveCharacterTextSplitter(

        # 设置子块的最大长度
        chunk_size=child_chunk_size,

        # 设置子块之间的重叠长度
        chunk_overlap=chunk_overlap,

        # 切割规则与父块保持一致
        separators=["\n\n", "\n", "。", "！", "？", " "],

        # 长度计算方式保持一致
        length_function=len
    )

    # 定义空列表，用于存储最终的【父+子】结构数据
    result = []

    # 遍历每一个父块，将其切成子块
    for parent in parent_chunks:

        # 将当前父块切成多个小子块
        child_chunks = child_splitter.split_text(parent)

        # 将【父块 + 对应的所有子块】打包成字典，存入结果列表
        result.append({
            "parent_chunk": parent,       # 完整语义父块
            "child_chunks": child_chunks  # 检索用子块列表
        })

    # 返回最终的父子分块结果
    return result


# ====================== 简化调用接口 ======================
def parent_chunk_split(text: str) -> List[Dict]:
    """
    对外统一调用的简化版函数
    作用：让外部调用更简单，不用传一堆参数
    """
    # 调用上面完整的父子分块函数，并使用默认配置
    return parent_child_split(
        text=text,
        parent_chunk_size=1024,
        child_chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )