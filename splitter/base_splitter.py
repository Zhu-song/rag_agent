#============================= RAG基础切片器==================================================

# -*- coding: utf-8 -*-
"""
基础文本分块器
作用：将长文本切成固定长度的小片段，用于 RAG 向量化
"""

# 导入 LangChain 官方推荐的递归分块s
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 从你的配置文件导入分块大小、重叠长度
from .config import CHUNK_SIZE, CHUNK_OVERLAP


def base_split(text: str) -> list[str]:
    """
    基础文本分块函数
    :param text: 输入的原始长文本
    :return: 分块后的文本列表
    """
    # 初始化分块器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", "。", "！", "？", " "],
        length_function=len
    )

    # 执行分块并返回结果
    return text_splitter.split_text(text)