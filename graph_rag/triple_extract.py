import json
from typing import List, Dict

# 导入大模型
from langchain_community.chat_models import ChatZhipuAI
# 从项目配置文件读取 API Key 和模型名称
from config import ZHIPU_API_KEY, ZHIPU_MODEL

# ====================== 初始化大模型 ======================
"""
这里创建一个大模型实例，用于后续的三元组抽取
所有配置都来自 config.py，统一管理
"""
llm = ChatZhipuAI(
    api_key=ZHIPU_API_KEY,
    model=ZHIPU_MODEL,
    temperature=0.1  # 温度越低，输出越稳定、越严谨
)

# ====================== 核心抽取提示词 ======================
"""
提示词模板：告诉大模型要做什么、输出什么格式
{{ }} 是为了转义，避免和 Python 的 format 冲突
"""
TRIPLE_EXTRACT_PROMPT = """
你是一名专业的知识图谱抽取引擎。
任务：从用户输入的文本中抽取【实体-关系-实体】三元组。

规则：
1.只输出标准 JSON 数组，不要任何解释、废话、标点、markdown。
2.格式严格为：
[{{"head":"头实体","relation":"关系","tail":"尾实体"}}]
3.只抽取有意义的实体，不要细碎内容。
4.无内容则返回[]。

待抽取文本：
{text}
"""

# ====================== 核心抽取函数 ======================
def extract_triples(text: str) -> List[Dict]:
    """
    从一段文本中抽取结构化三元组
    :param text: 输入的文本内容
    :return: 三元组列表，格式 [{"head":"","relation":"","tail":""}, ...]
    """
    # 把文本填入提示词模板
    prompt = TRIPLE_EXTRACT_PROMPT.format(text=text)
    
    # 调用大模型接口
    response = llm.invoke(prompt)
    
    # AIMessage 对象必须取 .content 才是真正的文本结果
    response_content = response.content.strip()
    
    # 把大模型返回的 JSON 字符串转成 Python 列表/字典
    try:
        triples = json.loads(response_content)
        # 确保返回的是列表
        return triples if isinstance(triples, list) else []
    except Exception as e:
        # 解析失败时打印错误，返回空列表
        print(f"[错误]三元组解析失败：{e}")
        return []

# ====================== 测试代码 ======================
if __name__ == "__main__":
    # 测试文本
    test_text = "张三在腾讯公司担任算法工程师，他精通Python和模型技术。"
    
    # 调用抽取函数
    result = extract_triples(test_text)
    
    # 输出结果
    print("抽取成功：")
    for t in result:
        print(t)