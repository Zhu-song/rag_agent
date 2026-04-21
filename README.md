# 🤖 RAG + Agent + MCP 智能知识库问答系统

基于 **RAG（检索增强生成）** + **ReAct Agent（智能体）** + **MCP（多工具调度平台）** 构建的智能知识库问答系统。

集成了智谱 GLM 大模型、FAISS 向量检索、BM25 关键词检索、混合检索、文档加载、文本分块、查询改写等完整 RAG 流程，同时支持 Agent 自主调用工具（计算器、文件读取、网络搜索、RAG 检索）完成复杂任务。

---

## 📁 项目结构

```
├── main.py                  # 项目入口（启动 FastAPI 服务）
├── config.py                # 全局配置（模型、RAG、Agent、MCP）
├── requirements.txt         # Python 依赖
├── .env                     # 环境变量（API Key 等）
│
├── llm/                     # 大模型模块
│   ├── chat_model.py        #   智谱 GLM 客户端（兼容 OpenAI 协议）
│   ├── memory.py            #   多轮对话记忆
│   └── prompt_template.py   #   提示词模板
│
├── loader/                  # 文档加载模块
│   ├── doc_loader.py        #   DOCX 文档加载
│   ├── pdf_loader.py        #   PDF 文档加载
│   ├── text_loader.py       #   TXT 文本加载
│   └── url_loader.py        #   URL 网页加载
│
├── splitter/                # 文本分块模块
│   ├── base_splitter.py     #   基础递归分块
│   ├── semantic_splitter.py #   语义分块
│   └── parent_chunk.py      #   父子块双层分块
│
├── retriever/               # 检索模块
│   ├── embedding.py         #   文本嵌入（智谱 API）
│   ├── vector_store.py      #   FAISS 向量库管理
│   ├── bm25_retriever.py    #   BM25 关键词检索
│   ├── hybrid_retriever.py  #   混合检索（向量 + BM25）
│   └── rerank.py            #   重排序
│
├── chain/                   # RAG 链模块
│   ├── rag_chain.py         #   基础 RAG 问答链
│   ├── adaptive_rag.py      #   自适应 RAG 入口
│   └── query_rewrite.py     #   查询改写（优化检索）
│
├── agent/                   # 智能体模块
│   ├── base_agent.py        #   Agent 抽象基类（ReAct 模式）
│   ├── react_agent.py       #   ReAct 智能体实现
│   ├── planner.py           #   任务规划器（问题拆分）
│   ├── executor.py          #   任务执行器
│   └── mcp/                 #   Agent 专用 MCP 子模块
│       ├── scheduler.py     #     工具调度器
│       └── tool_registry.py #     工具注册表
│
├── mcp/                     # MCP 多工具调度平台
│   ├── config.py            #   MCP 配置
│   ├── tool_registry.py     #   工具注册中心（单例）
│   ├── scheduler.py         #   工具调度器（执行 + 批量）
│   ├── tool_executor.py     #   工具执行封装（门面）
│   └── tool_manager.py      #   工具管理器（启用/禁用）
│
├── tools/                   # MCP 工具集
│   ├── calc_tool.py         #   计算器工具
│   ├── file_tool.py         #   文件读取工具
│   ├── rag_tool.py          #   RAG 检索工具
│   └── search_tool.py       #   联网搜索工具
│
├── api/                     # FastAPI Web 服务
│   ├── app.py               #   API 路由与启动
│   ├── schema.py            #   请求/响应模型
│   └── templates/           #   前端页面
│       └── index.html
│
└── utils/                   # 工具模块
    ├── logger.py            #   日志配置
    ├── text_process.py      #   文本处理工具
    └── eval_metrics.py      #   RAG 评测指标
```

---

## 🏗️ 系统架构

```
用户提问
   │
   ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  FastAPI    │────▶│  ReAct Agent  │────▶│  MCP 调度平台    │
│  Web 服务   │     │  (思考→行动→观察)│     │  (工具注册/调度) │
└─────────────┘     └──────┬───────┘     └────────┬────────┘
                           │                      │
              ┌────────────┼────────────┐          │
              ▼            ▼            ▼          ▼
         ┌────────┐  ┌──────────┐  ┌───────┐  ┌────────┐
         │ 规划器  │  │ 执行器   │  │ RAG   │  │ 计算器  │
         │Planner │  │Executor  │  │ 检索  │  │ 文件   │
         └────────┘  └──────────┘  │ 链    │  │ 搜索   │
                                   └───┬───┘  └────────┘
                                       │
                          ┌────────────┼────────────┐
                          ▼            ▼            ▼
                    ┌──────────┐ ┌──────────┐ ┌──────────┐
                    │ FAISS    │ │  BM25    │ │ 智谱 GLM │
                    │ 向量检索  │ │ 关键词   │ │ 大模型   │
                    └──────────┘ └──────────┘ └──────────┘
```

---

## 🚀 快速开始

### 1. 环境要求

- Python 3.9+
- 智谱 AI API Key（[免费申请](https://open.bigmodel.cn/)）

### 2. 克隆项目

```bash
git clone https://github.com/Zhu-song/rag_agent.git
cd your-repo
```

### 3. 创建虚拟环境并安装依赖

```bash
python -m venv venv
source venv/bin/activate    # macOS/Linux
# venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 4. 配置环境变量

复制并编辑 `.env` 文件，填入你的智谱 API Key：

```bash
ZHIPU_API_KEY=your_api_key_here
```

### 5. 启动服务

```bash
python main.py
```

服务启动后访问：**http://127.0.0.1:8000**

---

## 📡 API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/` | 前端页面 |
| `GET` | `/test` | 测试智谱 API 连接 |
| `POST` | `/api/chat` | 问答接口 |
| `GET` | `/api/health` | 健康检查 |

### 问答接口示例

```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "什么是RAG？", "rewrite": true}'
```

---

## 🔧 核心模块说明

### RAG 检索流程

```
文档加载 → 文本分块 → 向量化 → 存入 FAISS
                                      │
用户提问 → 查询改写 → 混合检索(向量+BM25) → 重排序 → LLM 生成答案
```

- **文档加载**：支持 PDF、DOCX、TXT、URL 四种来源
- **文本分块**：基础分块 / 语义分块 / 父子块双层分块
- **混合检索**：FAISS 向量检索（60%）+ BM25 关键词检索（40%）
- **查询改写**：对口语化问题进行优化，提升检索准确率

### ReAct Agent

采用 **ReAct（Reasoning + Acting）** 范式，循环执行：

1. **Think**：分析问题，决定是否调用工具
2. **Act**：执行工具调用或直接回答
3. **Observe**：整理工具执行结果
4. 循环直到得出最终答案

### MCP 工具调度

| 工具 | 说明 |
|------|------|
| `rag_retrieval` | 从本地知识库检索相关文档 |
| `calculator` | 数学计算 |
| `file_reader` | 读取本地文件 |
| `web_search` | 联网搜索实时信息 |

---

## ⚙️ 配置说明

所有配置集中在 `config.py` 中：

```python
# LLM 配置
ZHIPU_MODEL = "glm-4"              # 模型名称
LLM_TEMPERATURE = 0.1              # 生成温度
LLM_MAX_TOKENS = 4096              # 最大 token 数

# RAG 配置
CHUNK_SIZE = 512                   # 分块大小
CHUNK_OVERLAP = 50                 # 分块重叠
RETRIEVE_TOP_K = 6                 # 检索召回数量
RERANK_TOP_N = 3                   # 重排序数量

# Agent 配置
AGENT_MAX_ITERATIONS = 10          # 最大迭代次数
AGENT_THINKING_TIMEOUT = 30        # 思考超时时间（秒）

# MCP 配置
MCP_TOOL_TIMEOUT = 20              # 工具执行超时（秒）
MCP_MAX_PARALLEL_TOOLS = 3         # 最大并行工具数
```

---

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 大模型 | 智谱 GLM-4（OpenAI 兼容协议） |
| Web 框架 | FastAPI + Uvicorn |
| 向量数据库 | FAISS |
| 关键词检索 | BM25 (rank-bm25) |
| 文本分块 | LangChain Text Splitters |
| 文档解析 | pdfplumber、python-docx、BeautifulSoup |
| 嵌入模型 | 智谱 embedding-3 |
| Agent 框架 | 自研 ReAct Agent |
| 工具调度 | 自研 MCP 平台 |

---

## 📄 License

MIT License
