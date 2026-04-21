#=============================== 文本加载器 =========================================
# loader/txt_loader.py
import logging

logger = logging.getLogger(__name__)

def load_txt(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"加载文本文件失败: {file_path}, 错误: {e}")
        return ""
