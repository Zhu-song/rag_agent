# ================== 强制项目路径（必加，解决导入错误）==================
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
# ======================================================

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from pydantic import BaseModel  # 新增：用于接收前端JSON参数

# 导入项目配置（适配你的 config.py 和 .env）
from config import DOCS_DIR, VECTOR_DB_DIR, LLM_CONFIG
from langchain_openai import ChatOpenAI

# 导入 RAG 链（对接知识库检索）
from chain.rag_chain import rag_answer
from chain.query_rewrite import rewrite_query

# 导入 GraphRAG 知识图谱问答管线
from graph_rag.kgqa_pipeline import KGQAPipeline

# 初始化 FastAPI 应用
app = FastAPI(title="RAG 知识库问答系统", version="2.0")

# 跨域配置（解决前端跨域问题，确保前端能正常调用接口）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 获取当前文件所在目录（api/）
API_DIR = Path(__file__).parent

# 挂载静态文件（指向前端目录 api/templates）
app.mount("/static", StaticFiles(directory=str(API_DIR / "templates")), name="static")

# 初始化智谱 LLM（从 config 读取配置，密钥来自 .env）
llm = ChatOpenAI(
    api_key=LLM_CONFIG["api_key"],
    base_url=LLM_CONFIG["base_url"],
    model=LLM_CONFIG["model_name"],
    temperature=LLM_CONFIG["temperature"],
    max_tokens=LLM_CONFIG["max_tokens"],
    timeout=LLM_CONFIG["timeout"],
)

# 初始化 GraphRAG 知识图谱问答管线（启动时创建，全局复用）
kgqa_pipeline = KGQAPipeline()

# 新增：定义请求模型，匹配前端JSON参数
class ChatRequest(BaseModel):
    question: str
    rewrite: bool = True

# ------------------- 前端页面路由（加载 index.html）-------------------
@app.get("/")
async def serve_frontend():
    return FileResponse(str(API_DIR / "templates" / "index.html"))

# ------------------- 测试接口（测试智谱 API 连接）-------------------
@app.get("/test")
async def test_llm():
    try:
        # 发送简单测试请求，验证智谱连接
        response = llm.invoke("你好，简单介绍一下你自己")
        return {
            "code": 200,
            "msg": "✅ 智谱 API 连接成功！",
            "data": response.content
        }
    except Exception as e:
        return {
            "code": 500,
            "msg": "❌ 智谱 API 连接失败",
            "error": str(e)
        }

# ------------------- 正式问答接口（对接前端提问功能）-------------------
@app.post("/api/chat")
async def chat(request: ChatRequest):  # 修改：接收定义好的请求模型
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="问题不能为空")
    
    try:
        # 查询改写（可选）
        if request.rewrite:
            question = rewrite_query(question)
        
        # 使用 GraphRAG 管线（内部自动路由：知识图谱 or 向量检索）
        answer = kgqa_pipeline.ask(question, vector_rag_func=rag_answer)
        route = "graph_rag"
    except Exception as e:
        # 如果 GraphRAG 失败，降级为直接调用 LLM
        answer = llm.invoke(question).content
        route = "llm_fallback"
    
    return {
        "code": 0,
        "query": question,
        "answer": answer,
        "route": route
    }

# ------------------- 健康检查接口（验证服务是否正常）-------------------
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "RAG 知识库服务正常运行"}

# ------------------- 文件上传接口（上传文档到知识库）-------------------
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    # 校验文件类型
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"不支持的文件格式：{ext}，仅支持 {', '.join(ALLOWED_EXTENSIONS)}")

    # 保存文件到 docs/ 目录
    save_path = DOCS_DIR / file.filename
    try:
        with open(save_path, "wb") as f:
            content = await file.read()
            f.write(content)
        return {
            "code": 200,
            "msg": f"✅ 文件上传成功！",
            "filename": file.filename,
            "size": len(content),
            "path": str(save_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败：{str(e)}")

# ------------------- 查询已上传文件列表-------------------
@app.get("/api/files")
async def list_files():
    files = []
    for f in DOCS_DIR.iterdir():
        if f.is_file() and f.suffix.lower() in ALLOWED_EXTENSIONS:
            files.append({
                "name": f.name,
                "size": f.stat().st_size,
                "path": str(f)
            })
    return {"code": 200, "files": files, "total": len(files)}

# ------------------- 删除已上传文件-------------------
@app.delete("/api/files/{filename}")
async def delete_file(filename: str):
    file_path = DOCS_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="不允许删除此类型文件")
    try:
        file_path.unlink()
        return {"code": 200, "msg": f"✅ 已删除 {filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败：{str(e)}")

# ------------------- 构建知识库（上传文档后一键向量化）-------------------
@app.post("/api/build_kb")
async def build_knowledge_base():
    """读取 docs/ 下所有文档 → 分块 → 向量化 → 保存到 FAISS"""
    import glob
    from langchain_core.documents import Document
    from retriever.vector_store import save_vector_store
    from splitter.semantic_splitter import SemanticSplitter

    try:
        # 1. 收集所有文档
        all_docs = []
        for ext in ALLOWED_EXTENSIONS:
            for fp in DOCS_DIR.glob(f"*{ext}"):
                text = ""
                if ext == ".txt" or ext == ".md":
                    text = fp.read_text(encoding="utf-8", errors="ignore")
                elif ext == ".docx":
                    from loader.doc_loader import load_docx
                    text = load_docx(str(fp))
                elif ext == ".pdf":
                    from loader.pdf_loader import load_pdf
                    text = load_pdf(str(fp))

                if text.strip():
                    all_docs.append(Document(page_content=text, metadata={"source": fp.name}))

        if not all_docs:
            return {"code": 400, "msg": "❌ docs/ 目录下没有可用的文档"}

        # 2. 分块
        splitter = SemanticSplitter()
        chunks = []
        for doc in all_docs:
            chunks.extend(splitter.split_text(doc.page_content))

        # 3. 向量化保存
        save_vector_store(chunks)

        return {
            "code": 200,
            "msg": f"✅ 知识库构建成功！共处理 {len(all_docs)} 个文档，生成 {len(chunks)} 个文本块"
        }
    except Exception as e:
        return {"code": 500, "msg": f"❌ 构建失败：{str(e)}"}

# ------------------- Agent 模式问答接口-------------------
@app.post("/api/agent_chat")
async def agent_chat(request: ChatRequest):
    """使用 Agent 智能体回答（支持工具调用）"""
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="问题不能为空")
    try:
        from agent.react_agent import ReActAgent
        agent = ReActAgent()
        result = agent.run(question)
        return {
            "code": 0,
            "query": question,
            "answer": result.get("answer", "无法获取答案"),
            "iterations": result.get("iterations", 0),
            "route": "agent"
        }
    except Exception as e:
        return {"code": 500, "msg": f"Agent 执行失败：{str(e)}"}
