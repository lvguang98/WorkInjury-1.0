import sqlite3
from contextlib import contextmanager
from typing import Iterator, List
from core.models import Person, InjuredPerson, Case
from core.exceptions import DatabaseError
import os
class CaseService:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()
        print(f"尝试打开数据库路径: {self.db_path}")
        print(f"路径是否存在: {os.path.exists(self.db_path)}")

    @contextmanager
    def _get_connection(self) -> Iterator[sqlite3.Connection]:
        """获取数据库连接"""
        print(f"尝试打开数据库路径: {self.db_path}")
        print(f"路径是否存在: {os.path.exists(self.db_path)}")
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        except sqlite3.Error as e:
            raise DatabaseError(f"数据库操作失败: {str(e)}")
        finally:
            conn.close()

    def _init_db(self):
        """初始化数据库表结构"""
        with self._get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS cases (
                    id TEXT PRIMARY KEY,
                    case_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    company TEXT,
                    construction_site TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS persons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_id TEXT NOT NULL,
                    type TEXT NOT NULL,
                    name TEXT NOT NULL,
                    id_card TEXT,
                    gender TEXT,
                    age INTEGER,
                    phone TEXT,
                    position TEXT,
                    FOREIGN KEY (case_id) REFERENCES cases (id)
                );
            """)

    def create_case(self, case: Case) -> str:
        """创建新案件"""
        with self._get_connection() as conn:
            try:
                # 保存案件基本信息
                conn.execute(
                    "INSERT INTO cases (id, case_type, status, company, construction_site) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (case.case_id, case.case_type, case.status,
                     case.company, case.construction_site)
                )

                # 保存受伤人员信息
                self._save_person(conn, case.case_id, "injured", case.injured_person)

                # 保存证人信息
                for witness in case.witnesses:
                    self._save_person(conn, case.case_id, "witness", witness)

                conn.commit()
                return case.case_id
            except sqlite3.Error as e:
                conn.rollback()
                raise DatabaseError(f"创建案件失败: {str(e)}")

    def _save_person(self, conn: sqlite3.Connection, case_id: str,
                     person_type: str, person: Person):
        """保存人员信息"""
        conn.execute(
            "INSERT INTO persons (case_id, type, name, id_card, gender, age, phone, position) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (case_id, person_type, person.name, person.id_card,
             person.gender, person.age, person.phone, person.position)
        )
