import sys
import warnings
warnings.filterwarnings("ignore")

# 项目根目录
sys.path.append("/Users/zhusong/Desktop/学习/rag_project")

# 测试
from chain.rag_chain import rag_answer

if __name__ == "__main__":
    print("测试 RAG 问答...")
    answer = rag_answer("你好")
    print("回答：", answer)