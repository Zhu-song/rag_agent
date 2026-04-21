#============================== 搜索工具 ==========================================
# tools/search_tool.py
# 导入 MCP 工具注册中心，用于把当前函数注册成 Agent 可调用工具
from mcp.tool_registry import tool_registry

# 导入 requests 库，用于发送 HTTP 请求实现联网搜索
import requests
import os

# 注册工具：将函数注册到 MCP 工具系统
@tool_registry.register(
    name="web_search",                  # 工具名称：Agent 调用时使用
    desc="联网搜索实时信息",            # 工具描述：给大模型看，让它知道什么时候调用
    params_schema={"query": "搜索关键词"}  # 参数说明：告诉模型需要传入搜索词
)
def web_search_tool(query: str):
    """
    联网搜索工具（免费 Jina AI 搜索接口）
    功能：根据用户的查询关键词，获取互联网实时信息
    :param query: 用户要搜索的问题/关键词
    :return: 搜索结果列表 或 错误信息
    """
    try:
        # 定义 Jina AI 搜索接口地址（免费联网搜索服务）
        url = "https://api.jina.ai/v1/search"
        
        # 请求头：携带 API Key 进行身份验证
        headers = {
            "Authorization": f"Bearer {os.getenv('JINA_API_KEY', '')}"
        }
        
        # 请求参数：搜索词 + 最多返回 2 条结果
        data = {
            "q": query,        # 搜索关键词
            "max_results": 2   # 最多返回2条结果，避免内容过长
        }

        # 发送 POST 请求，调用搜索接口（超时10秒）
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        
        # 将接口返回的 JSON 数据转为 Python 字典
        results = resp.json()

        # 如果返回结果中有 data 字段，说明搜索成功
        if "data" in results:
            # 格式化结果：只保留标题 + 前800字符内容
            return [
                {
                    "title": item.get("title"),    # 文章标题
                    "content": (item.get("content") or "")[:800]  # 内容（截断800字符）
                }
                for item in results["data"]
            ]
        
        # 没有 data 字段 → 未搜索到内容
        return "未搜索到相关内容"

    # 捕获所有异常（网络错误、接口失败、超时等）
    except Exception as e:
        return f"搜索失败：{str(e)}"