class MockResponse:
    def __init__(self, content):
        self.content = content

def get_chat_llm():
    class MockLLM:
        def invoke(self, prompt):
            return MockResponse('''{"thought":"计算问题","tool_name":"calculator","tool_params":{"a":3,"b":15,"op":"mul"},"need_continue":false}''')
    return MockLLM()