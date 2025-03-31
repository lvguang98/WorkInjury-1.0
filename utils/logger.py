import logging
import sys
from pathlib import Path


def setup_logging():
    """配置日志系统"""
    logs_dir = Path(__file__).parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(logs_dir / "app.log", encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    # 设置第三方库日志级别
    logging.getLogger('PyQt5').setLevel(logging.WARNING)