#============================= 计算工具 ===========================================
from mcp.tool_registry import tool_registry

# 使用装饰器，将当前函数注册到 MCP 工具中心
@tool_registry.register(
    name="calculator",                  # 工具名称：Agent/MCP 调用时使用的名字
    desc="计算器，支持加减乘除",         # 工具描述：给大模型看，让它知道这个工具的用途
    params_schema={                     # 参数说明：告诉模型需要传什么参数
        "a": "数字1",
        "b": "数字2",
        "op": "操作符 + - * /"
    }
)
def calc_tool(a: float, b: float, op: str):
    """
    计算器工具的真实执行函数
    :param a: 第一个数字（浮点数）
    :param b: 第二个数字（浮点数）
    :param op: 操作符，支持 + - * /
    :return: 计算结果 或 错误提示
    """
    # 加法
    if op == "+":
        return a + b
    # 减法
    elif op == "-":
        return a - b
    # 乘法
    elif op == "*":
        return a * b
    # 除法：增加除数不能为 0 的安全判断
    elif op == "/":
        return a / b if b != 0 else "除数不能为0"
    # 不支持的操作符
    else:
        return "不支持的操作符"