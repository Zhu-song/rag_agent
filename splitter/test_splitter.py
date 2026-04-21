# -*- coding: utf-8 -*-
"""
分块器测试文件
测试：base_split / semantic_split / parent_chunk_split
"""

# ----------------------
# 导入你的三个分块工具
# ----------------------
from base_splitter import base_split
from semantic_splitter import semantic_split
from parent_chunk import parent_chunk_split

# ----------------------
# 测试用长文本
# ----------------------
TEST_TEXT = """
RAG是检索增强生成（Retrieval Augmented Generation）的简称。
它的核心流程是：读取文档 → 文本分块 → 向量化 → 存入向量库 → 用户提问检索 → 交给大模型生成回答。

文本分块是RAG中非常关键的一步，分块好坏直接决定最终回答效果。
常见分块方式有：基础长度分块、语义分块、父子分块。

基础分块按长度切割，语义分块按段落切割，父子分块先切大块再切小块，检索更精准。
"""

# ----------------------
# 开始测试
# ----------------------
if __name__ == "__main__":
    print("=" * 60)
    print("🧪 开始测试 RAG 分块器模块")
    print("=" * 60)

    # 1. 测试基础分块
    print("\n📌 测试 1：基础分块 base_split")
    base_chunks = base_split(TEST_TEXT)
    for idx, c in enumerate(base_chunks):
        print(f"[{idx+1}] {c}")
    print(f"✅ 基础分块完成，共 {len(base_chunks)} 块")

    # 2. 测试语义分块
    print("\n📌 测试 2：语义分块 semantic_split")
    semantic_chunks = semantic_split(TEST_TEXT)
    for idx, c in enumerate(semantic_chunks):
        print(f"[{idx+1}] {c}")
    print(f"✅ 语义分块完成，共 {len(semantic_chunks)} 块")

    # 3. 测试父子分块（高级）
    print("\n📌 测试 3：父子分块 parent_chunk_split")
    parent_chunks = parent_chunk_split(TEST_TEXT)
    for idx, item in enumerate(parent_chunks):
        print(f"\n===== 父块 {idx+1} =====")
        print(item["parent_chunk"])
    print(f"✅ 父子分块完成，共 {len(parent_chunks)} 个父块")

    print("\n" + "=" * 60)
    print("🎉 所有分块器测试：全部通过！")
    print("=" * 60)