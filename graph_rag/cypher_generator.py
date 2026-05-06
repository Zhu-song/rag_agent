import json
# 导入大模型
from langchain_community.chat_models import ChatZhipuAI
# 从项目配置文件读取 API Key 和模型名称
from config import ZHIPU_API_KEY, ZHIPU_MODEL

# ====================== 初始化大模型 ======================
"""
这里创建一个大模型实例，用于后续的Cypher语句生成
所有配置都来自 config.py，统一管理
"""
llm = ChatZhipuAI(
    api_key=ZHIPU_API_KEY,
    model=ZHIPU_MODEL,
    temperature=0.1  # 温度越低，输出越稳定、越严谨
)

# ====================== 核心 Prompt ======================
"""
Cypher 生成提示词模板：
根据用户的自然语言问题，生成可以直接在 Neo4j 中运行的查询语句
"""
CYPHER_GENERATE_PROMPT = """
你是一个专业的Neo4j Cypher语句生成专家，只会输出合法Cypher语句。
数据库节点标签：实体
节点属性：name
关系：直接使用关系名称

规则：
1.只输出纯 Cypher 语句，不要任何解释、文字、markdown、括号、注释。
2.节点匹配使用：MATCH (p:实体{{name:"实体名"}})
3.关系直接写名称，不要加引号。
4.必须是可执行运行的正确语法。

用户问题：{question}
生成Cypher:
"""

def extract_entities(question:str)->list:
    """
    从问题中抽取关键实体（给LLM做简单抽取）
    :param question: 用户的问题
    :return: 抽取到的实体列表
    """
    prompt = f"""从问题中抽取出所有实体名词，用JSON数组返回，不要其他内容：
    问题：{question}
    输出：[]"""
    
    try:
        # 调用大模型抽取实体
        resp = llm.invoke(prompt)
        # 解析返回的JSON结果
        return json.loads(resp.content.strip())
    except:
        # 异常时返回空列表
        return []

def generate_cypher(question:str)->str:
    """
    输入自然语言问题→输出可直接运行的 Cypher 语句
    :param question: 用户问题
    :return: 可直接执行的 Cypher 查询语句
    """
    # 抽取问题中的实体
    entities = extract_entities(question)
    
    # 拼接提示词，生成 Cypher
    prompt = CYPHER_GENERATE_PROMPT.format(question=question)
    # 调用模型并获取返回内容
    cypher = llm.invoke(prompt).content.strip()
    
    # 清理多余符号，保证纯 Cypher 语句
    cypher = cypher.replace("```cypher", "").replace("```", "").strip()
    return cypher


# ====================== 测试 ======================
if __name__ =="__main__":
    # 测试问题
    question ="张三精通什么？"
    
    # 生成 Cypher 语句
    cypher = generate_cypher(question)
    print("🤖 生成的 Cypher 语句：")
    print(cypher)