# api/schema.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ChatRequest(BaseModel):
    query: str
    use_agent: bool = True  # True=用Agent+MCP，False=直接RAG


class ChatResponse(BaseModel):
    query: str
    answer: str
    use_agent: bool
    iterations: Optional[int] = None
    history: Optional[List[Dict[str, Any]]] = None


class ToolCallLog(BaseModel):
    tool_name: str
    params: Dict[str, Any]
    result: Any