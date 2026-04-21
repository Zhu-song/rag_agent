#============================== URL加载器 ==========================================
# loader/url_loader.py
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def load_url(url: str):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.get_text(strip=True)
    except Exception as e:
        logger.error(f"加载URL失败: {url}, 错误: {e}")
        return ""
