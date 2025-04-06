import json
import os
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


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
            },
            "case_counter": 1,  # 新增案件计数器
            "last_case_date": datetime.now().strftime("%Y%m%d")  # 记录最后案件日期
        }
        self.data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 合并默认配置（防止旧配置缺少新增字段）
                return {**self.default_config, **config}
        return self.default_config

    def save(self):
        """保存配置"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get_database_path(self) -> str:
        """获取数据库路径"""
        return self.data["database"]["path"]

    def generate_case_id(self) -> str:
        """
        生成连续的案件编号
        格式: CASE-YYYYMMDD-XXX (每日重置序号)
        """
        today = datetime.now().strftime("%Y%m%d")

        # 如果是新的一天，重置计数器
        if self.data["last_case_date"] != today:
            self.data["case_counter"] = 1
            self.data["last_case_date"] = today

        case_id = f"CASE-{today}-{self.data['case_counter']:03d}"

        # 递增并保存
        self.data["case_counter"] += 1
        self.save()

        return case_id