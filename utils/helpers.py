import os
from typing import Optional

def generate_case_id() -> str:
    """生成案件ID"""
    import uuid
    return f"case-{uuid.uuid4().hex[:8]}"

def ensure_directory(path: str) -> str:
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)
    return path