import json
import os
from pathlib import Path
from typing import Dict, Any


class Config:
    def __init__(self):
        self.app_dir = Path(__file__).parent
        self.config_path = self.app_dir / "config.json"
        self.default_config = {
            "database": {
                "path": str(self.app_dir / "data" / "database.db"),
                "type": "sqlite"
            },
            "ui": {
                "theme": "light",
                "font_size": 12,
                "window_size": [800, 600]
            }
        }
        self.data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.default_config

    def save(self):
        """保存配置"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get_database_path(self) -> str:
        """获取数据库路径"""
        return self.data["database"]["path"]