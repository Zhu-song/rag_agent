from neo4j import GraphDatabase
from typing import List,Dict
from config import NEO4J_URI,NEO4J_USER,NEO4J_PASSWORD

class Neo4jClient:
    """
    Neo4j知识图谱客户端工具类
    作用：封装所有Neo4j数据库的操作（连接、存数据、查数据、清空）
    整个项目的数据库核心模块
    """
    
    def __init__(self):
        """
        初始化方法：创建数据库连接
        类被实例化时自动执行，建立到Neo4j的连接
        """
        self.driver = GraphDatabase.driver(
            NEO4J_URI,        #数据库地址
            auth=(NEO4J_USER,NEO4J_PASSWORD)   #账号密码
        )
            
        
    def close(self):
        """
        关闭数据库连接
        使用完毕后必须调用，释放资源
        """
        self.driver.close()
        
    def run(self,cypher:str,params: dict = None):
        """执行任意Cypher语句"""
        with self.driver.session() as session:
            return session.run(cypher,parameters=params or {})
    
    def create_node(self,name:str,node_type:str = "实体"):
        """创建节点（存在则忽略，去重）"""
        cypher = """
        MERGE (n:实体{name:$name})
        SET n.type = $type
        """
        self.run(cypher,{"name":name,"type":node_type})
    
    def create_relation(self,head:str,relation:str,tail:str):
        """创建关系：头实体 -[关系]->尾实体"""
        # 安全处理关系名称，防止 Cypher 注入
        safe_relation = "".join(c if c.isalnum() or c == "_" else "_" for c in relation)
        cypher = f"""
        MATCH (a:实体{{name:$head}}), (b:实体{{name:$tail}})
        MERGE (a)-[r:{safe_relation}]->(b)
        """
        self.run(cypher,{"head":head,"tail":tail})
        
    def batch_import_triples(self,triples:List[Dict]):
        """批量导入归一化后的三元组(第3天输出结果)
        :param triples:[{"head":"","relation":"","tail":""},...]
        """
        for t in triples:
            head = t.get("head", "").strip()
            relation = t.get("relation", "").strip()
            tail = t.get("tail", "").strip()
            
            if not head or not relation or not tail:
                continue
            
            # 创建节点
            self.create_node(head)
            self.create_node(tail)
            
            #创建关系
            self.create_relation(head,relation,tail)
            
        print(f"✅ 批量入库完成，共 {len(triples)} 条三元组")
        
    def clear_all(self):
        """清空数据库（开发调试用）"""
        self.run("MATCH (n) DETACH DELETE n")
        print("🗑️ 已清空所有数据")
        
# ====================== 测试 ======================
if __name__ == "__main__":
    # 测试用（第3天输出的干净三元组）
    test_data = [
        {"head": "张三", "relation": "任职于", "tail": "腾讯"},
        {"head": "张三", "relation": "精通", "tail": "Python"},
        {"head": "Python", "relation": "属于", "tail": "编程语言"}
    ]

    # 初始化客户端
    client = Neo4jClient()
    
    # 清空再导入（测试用）
    client.clear_all()
    
    # 批量入库
    client.batch_import_triples(test_data)
    
    print("🎉 Neo4j 批量入库测试成功！")
    client.close()