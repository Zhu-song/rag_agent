#============================ 日志 ============================
import logging
from pathlib import Path
from config import LOG_FILE, LOG_LEVEL

logger = logging.getLogger("rag_agent")
logger.setLevel(LOG_LEVEL)
logger.handlers.clear()

fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")

fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
fh.setFormatter(fmt)

ch = logging.StreamHandler()
ch.setFormatter(fmt)

logger.addHandler(fh)
logger.addHandler(ch)
logger.propagate = False