# 解决相对导入报错！只改这个文件！
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

# ====================
# 强制修复 . 相对导入问题
# ====================
import tool_executor
tool_executor.__package__ = ""

from tool_registry import tool_registry
from scheduler import MCPScheduler
import tool_executor
from tool_manager import ToolManager

# 重新加载，修复 . 导入
import importlib
importlib.reload(tool_executor)

from tool_executor import MCPToolExecutor

# ------------------------------
# 注册测试工具
# ------------------------------
@tool_registry.register(
    name="calculator",
    desc="四则运算工具",
)
def calculator(a, b, op):
    if op == "add": return a + b
    if op == "sub": return a - b
    if op == "mul": return a * b
    if op == "div": return a / b
    return "错误"

# ------------------------------
# 开始测试
# ------------------------------
print("="*50)
print("测试 1：工具列表")
for t in tool_registry.list_tools():
    print(t)

print("\n测试 2：调度器 3*15")
s = MCPScheduler()
print(s.run_tool("calculator", a=3, b=15, op="mul"))

print("\n测试 3：执行器 100-37")
e = MCPToolExecutor()
print(e.invoke("calculator", {"a":100,"b":37,"op":"sub"}))

print("\n测试 4：工具开关")
m = ToolManager()
print("可用:", m.is_available("calculator"))

print("\n🎉 MCP 测试全部成功！")