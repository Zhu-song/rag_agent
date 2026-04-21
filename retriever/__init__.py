from .embedding import get_embedding
from .vector_store import get_vector_store, save_vector_store, get_faiss_retriever
from .bm25_retriever import get_bm25_retriever
from .hybrid_retriever import get_hybrid_retriever
from .rerank import rerank_documents


__all__ = [
    "get_embedding",
    "get_vector_store",
    "save_vector_store",
    "get_faiss_retriever",
    "get_bm25_retriever",
    "get_hybrid_retriever",
    "rerank_documents"
]

# 作用是把 retriever 文件夹变成一个 “可直接调用的工具包”，在其他地方只需要 import retriever 就可以使用里面的所有加载器函数了。

# 好处 1：简化外部调用，让使用更方便
# 好处 2：隐藏内部细节，提升代码可维护性
# 好处 3：统一接口，方便后续扩展新的加载器函数


# __all__ 是一个 “对外接口声明”，作用是：
# 1.当别人写 from retriever import * 时，只会导入你在 __all__ 里列出来的这 4 个函数，
# 不会把其他隐藏的函数 / 变量也暴露出去，避免污染别人的命名空间。
# 2.给 IDE 和用户一个明确的 “公开 API 列表”，告诉大家：这 4 个是我设计好、稳定可用的工
# 具，其他的都是内部实现，不要随便用。