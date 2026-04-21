import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ======================
# 基础路径
# ======================
BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"
VECTOR_DB_DIR = BASE_DIR / "vector_db"
LOG_DIR = BASE_DIR / "logs"

os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ======================
# LLM 配置（智谱）
# ======================
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
ZHIPU_MODEL = "glm-4"
ZHIPU_EMBEDDING_MODEL = "embedding-3"
LLM_TEMPERATURE = 0.1
LLM_MAX_TOKENS = 4096

# LLM 配置字典（供 ChatOpenAI 使用）
LLM_CONFIG = {
    "api_key": ZHIPU_API_KEY,
    "base_url": "https://open.bigmodel.cn/api/paas/v4",
    "model_name": ZHIPU_MODEL,
    "temperature": LLM_TEMPERATURE,
    "max_tokens": LLM_MAX_TOKENS,
    "timeout": 60,
}

# ======================
# RAG 配置
# ======================
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50
RETRIEVE_TOP_K = 6
RERANK_TOP_N = 3

# ======================
# Agent 核心配置
# ======================
AGENT_MAX_ITERATIONS = 10
AGENT_THINKING_TIMEOUT = 30
AGENT_ENABLE_PLANNER = True

# ======================
# MCP 多工具调度平台配置
# ======================
MCP_TOOL_TIMEOUT = 20
MCP_MAX_PARALLEL_TOOLS = 3
MCP_ENABLE_LOG = True
MCP_ALLOWED_TOOLS = [
    "rag_retrieval",
    "calculator",
    "file_reader",
    "web_search"
]

# ======================
# 日志
# ======================
LOG_LEVEL = "INFO"
LOG_FILE = LOG_DIR / "agent_mcp_rag.log"

# ======================
# API 服务
# ======================
API_HOST = "0.0.0.0"
API_PORT = 8000
API_RELOAD = True