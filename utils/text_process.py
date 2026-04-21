#================================== 文件清洗 ==================================
import re

def clean_text(text: str) -> str:
    # 多余空格、换行、制表符
    text = re.sub(r'\s+', ' ', text)
    # 多余标点
    text = re.sub(r'。+', '。', text)
    text = text.strip()
    return text

def split_long_text(text: str, max_len: int = 512) -> list[str]:
    return [text[i:i+max_len] for i in range(0, len(text), max_len)]