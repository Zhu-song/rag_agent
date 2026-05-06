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


# ====================== 实体归一化 Prompt ======================
NORMALIZE_PROMPT = """
你是实体归一化组手。请将输入的实体统一为标准名称，并分类。
规则：
1.别名、简称、全称统一成标准名称
2.输出严格JSON格式，不要任何解释
3.输出格式:{{"标准实体名":"XXX","实体类型":"人物/公司/技术/产品/文档/其他"}}
待归一化实体列表：
{entities}
"""

# ====================== 核心工具类 ======================
class EntityNormalizer:
    def __init__(self):
        """
        初始化实体归一化工具
        entity_map: 存放别名到标准实体名的映射
        type_map: 存放实体对应的类型
        """
        self.entity_map = {}  # 别名 → 标准名
        self.type_map = {}    # 实体 → 类型

    def normalize_entity(self, entity: str) -> str:
        """
        实体归一化：别名映射为标准名
        :param entity: 原始实体名
        :return: 标准实体名
        """
        return self.entity_map.get(entity, entity).strip()

    def clean_triples(self, triples: List[Dict]) -> List[Dict]:
        """
        清洗三元组：
        1.过滤空值
        2.实体归一化
        3.去重
        :param triples: 原始三元组列表
        :return: 清洗后的三元组列表
        """
        cleaned = []
        seen = set()
        for t in triples:
            head = t.get("head", "").strip()
            relation = t.get("relation", "").strip()
            tail = t.get("tail", "").strip()

            # 过滤空内容
            if not head or not relation or not tail:
                continue

            # 实体归一化
            head_std = self.normalize_entity(head)
            tail_std = self.normalize_entity(tail)

            # 去重
            key = (head_std, relation, tail_std)
            if key in seen:
                continue
            seen.add(key)

            cleaned.append({
                "head": head_std,
                "relation": relation,
                "tail": tail_std
            })
        return cleaned

    def batch_normalize(self, triples: List[Dict]) -> List[Dict]:
        """
        批量归一化所有实体（LLM对齐）
        :param triples: 待处理的三元组列表
        :return: 归一化后的三元组列表
        """
        # 收集所有出现的实体
        entities = set()
        for t in triples:
            entities.add(t.get("head", ""))
            entities.add(t.get("tail", ""))

        # 过滤空字符串
        entities = [e for e in entities if e]

        # 构造 LLM 归一化提示词
        prompt = NORMALIZE_PROMPT.format(entities=json.dumps(entities, ensure_ascii=False))
        # 调用大模型
        resp = llm.invoke(prompt)

        # 获取模型返回的文本内容
        res_content = resp.content.strip()

        try:
            # 解析返回的 JSON
            result = json.loads(res_content)
            # 遍历结果，构建实体映射和类型映射
            for raw, std_info in result.items():
                std_name = std_info.get("标准实体名", raw)
                type_name = std_info.get("实体类型", "其他")
                self.entity_map[raw] = std_name
                self.type_map[std_name] = type_name
        except Exception as e:
            # 解析失败时打印错误信息
            print(f"[归一化错误]{e}")

        # 清洗并返回最终结果
        return self.clean_triples(triples)


# ====================== 测试 ======================
if __name__ == "__main__":
    # 测试用三元组（含别名、脏数据）
    test_triples = [
        {"head": "张三", "relation": "任职于", "tail": "腾讯"},
        {"head": "张三", "relation": "精通", "tail": "python"},
        {"head": "Python", "relation": "属于", "tail": "编程语言"},
        {"head": "张三", "relation": "精通", "tail": "python"},  # 重复
        {"head": "", "relation": "测试", "tail": "空数据"},  # 脏数据
    ]

    # 创建实体归一化对象
    norm = EntityNormalizer()
    # 执行批量归一化
    cleaned = norm.batch_normalize(test_triples)

    # 输出结果
    print("=== 清洗归一化后三元组 ===")
    for t in cleaned:
        print(t)