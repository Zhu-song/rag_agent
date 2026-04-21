#=========================================================== 语义切片器=====================
# -*- coding: utf-8 -*-
"""
语义分块器（Semantic Splitter）
作用：根据文本语义自动切分，比普通分块更适合 RAG，效果更强
不是按长度硬切，而是按“语义段落”切
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from .config import CHUNK_SIZE, CHUNK_OVERLAP


def semantic_split(text: str) -> List[str]:
    """
    语义分块：按中文段落 + 语义边界切分，更适合知识库、文档、小说、论文
    :param text: 原始长文本
    :return: 分块后的语义段落列表
    """

    # 语义分块规则：优先保留完整段落、完整句子
    splitter = RecursiveCharacterTextSplitter(

        # 最大块长度（和你的 base_splitter 保持一致，方便统一控制）
        chunk_size=CHUNK_SIZE,

        # 块重叠（保证上下文连贯）
        chunk_overlap=CHUNK_OVERLAP,

        # 【语义切割】按中文最强语义边界切割
        separators=[
            "\n\n\n",      # 大段落（最强语义）
            "\n\n",        # 段落
            "\n",          # 换行
            "。",          # 中文句子
            "！",
            "？",
            "；",
            "，",
            " "
        ],

        # 自动合并碎片，避免太短的块
        strip_whitespace=True,
    )

    # 执行分块
    chunks = splitter.split_text(text)

    # 过滤空块
    chunks = [c.strip() for c in chunks if c.strip()]

    return chunks