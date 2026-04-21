#============================== 文件工具 ==========================================
# 导入 MCP 工具注册中心，用于把当前函数注册成可调用工具
from mcp.tool_registry import tool_registry

# 导入配置：从 config 中获取文档存放的根目录
from config import DOCS_DIR

# 注册工具：告诉系统这是一个可供 Agent / MCP 调用的工具
@tool_registry.register(
    name="file_reader",          # 工具名称：调用时用这个名字
    desc="读取本地文档内容",     # 工具描述：给大模型看，让它知道用途
    params_schema={              # 参数说明：告诉模型需要传入什么参数
        "filename": "文件名（如：test.txt）"
    }
)
def file_reader_tool(filename: str):
    """
    本地文件读取工具
    功能：从 DOCS_DIR 目录下读取指定文本文件内容
    :param filename: 要读取的文件名
    :return: 文件内容（最多2000字符）或 错误信息
    """
    try:
        # 拼接路径：文档根目录 / 文件名
        path = DOCS_DIR / filename
        
        # 打开文件，以 utf-8 编码读取
        with open(path, "r", encoding="utf-8") as f:
            # 读取内容，最多返回前 2000 个字符，避免内容过长
            return f.read()[:2000]
    
    # 捕获所有异常（文件不存在、权限不足、格式错误等）
    except Exception as e:
        # 返回友好的错误提示
        return f"读取失败：{str(e)}"