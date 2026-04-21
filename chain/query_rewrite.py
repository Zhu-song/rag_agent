#======================== 查询改写（优化检索） ========================
# ===========================================================
# 查询改写模块（Query Rewriting）
# 功能：对用户的问题进行优化、润色、扩展，让检索更准确
# 解决：用户问题口语化、简短、模糊导致检索不到内容的问题
# ===========================================================

# 导入大模型（智谱AI / 通用大模型）
from llm.chat_model import get_chat_llm
# 导入提示词模板
from langchain_core.prompts import PromptTemplate


def rewrite_query(query: str) -> str:
    """
    对用户原始问题进行优化改写，使其更适合文档检索
    作用：
        1. 把口语化问题 → 改成标准书面问题
        2. 简化冗余内容 → 突出核心意图
        3. 让检索更容易匹配到相关文档
        4. 提升 RAG 整体回答准确率

    参数：
        query: 用户原始问题
    返回：
        优化改写后的标准问题
    """
    # 1. 获取大模型实例
    llm = get_chat_llm()

    # 2. 定义查询改写提示词模板
    prompt = PromptTemplate(
        input_variables=["query"],
        template="将以下用户问题优化为适合文档检索的标准问题：\n问题：{query}\n优化后："
    )

    # 3. 构建提示词 → 大模型 的执行链
    chain = prompt | llm
    
    # 4. 执行链，传入用户问题
    res = chain.invoke({"query": query})
    
    # 5. 返回清理后的改写结果（去掉空格、换行）
    return res.content.strip() if hasattr(res, 'content') else str(res).strip()