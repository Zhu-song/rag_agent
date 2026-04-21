#============================= PDF加载器 ===========================================
# loader/pdf_loader.py
import logging
import pdfplumber

logger = logging.getLogger(__name__)

def load_pdf(file_path: str):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t
    except Exception as e:
        logger.error(f"加载PDF失败: {file_path}, 错误: {e}")
    return text
