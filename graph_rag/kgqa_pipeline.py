from graph_rag.neo4j_client import Neo4jClient
from graph_rag.cypher_generator import generate_cypher,extract_entities
# 导入大模型
from langchain_community.chat_models import ChatZhipuAI
# 从项目配置文件读取 API Key 和模型名称
from config import ZHIPU_API_KEY, ZHIPU_MODEL


from chain.rag_chain import rag_answer
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
# ====================== 路由判断 Prompt ======================
ROUTE_PROMPT = """
你是问题路由专家。判断用户问题应该用【知识图谱查询】还是【向量检索】。
规则：
1.问题包含实体、关系、人物、公司、技术、推理 → 回答：graph
2.问题是总结、解释、语义模糊、文章内容 → 回答：vector
3.只输出graph或vector，不要其他内容

问题:{question}
输出：
"""
# ====================== 答案融合 Prompt ======================
ANSWER_PROMPT = """
根据提供的知识图谱查询结果，整理成自然语言回答用户。
如何没有结果，就说“未找到相关信息”。

用户问题:{question}
图谱查询结果:{kg_result}
回答：
"""
class KGQAPipeline:
    def __init__(self):
        self.neo4j = Neo4jClient()
        
    def route_question(self,question:str)->str:
        """判断走图谱还是向量"""
        prompt = ROUTE_PROMPT.format(question=question)
        return llm.invoke(prompt).content.strip().lower()
    
    def query_graph(self,question:str)->str:
        """执行图谱查询"""
        try:
            #1.生成cypher
            cypher = generate_cypher(question)
            print(f"📊 执行 Cypher: {cypher}")
            
            #2.查询Neo4j
            with self.neo4j.driver.session() as session:
                result = session.run(cypher)
                records = [r.data() for r in result]
            
            
            #3.转字符串
            return str(records)
        except Exception as e:
            print(f"图谱查询失败:{e}")
            return ""
    
    def ask(self,question:str,vector_rag_func=None)->str:
        """
        对外总入口
        :param question:用户问题
        :param vector_rag_func:原有RAG的问答函数
        :return: 最终回答
        """
        # === 步骤1：路由判断 ===
        route = self.route_question(question)
        print(f"🔍 路由选择: {route}")
        
        # === 步骤2：执行查询 ===
        kg_result = ""
        vector_result = ""
        
        if route == "graph":
            kg_result = self.query_graph(question)
        else:
            vector_result = rag_answer(question)
        
        # === 步骤3：生成最终答案 ===
        final_prompt = ANSWER_PROMPT.format(
            question=question,
            kg_result=kg_result if route =="graph" else "向量检索结果：" +vector_result
        )
        
        return llm.invoke(final_prompt).content.strip()
    
# ====================== 测试 ======================
if __name__ == "__main__":
    # 初始化 KGQA 管道
    kgqa = KGQAPipeline()

    # 测试图谱问题
    q1 = "张三精通什么？"
    ans = kgqa.ask(q1)
    print("=" * 50)
    print(f"问题：{q1}")
    print(f"答案：{ans}")