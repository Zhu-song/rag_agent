#============================== DOC加载器 ==========================================
# loader/doc_loader.py
import logging
from docx import Document

logger = logging.getLogger(__name__)

def load_docx(file_path: str):
    text = ""
    try:
        doc = Document(file_path)
        for p in doc.paragraphs:
            text += p.text + "\n"
    except Exception as e:
        logger.error(f"加载DOCX失败: {file_path}, 错误: {e}")
    return text
