import sqlite3
from typing import Dict
from src.memory.memory_store import MemoryStore


class SqliteMemoryStore(MemoryStore):
    def __init__(self, db_path: str = "memory.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS facts (
                user_id INTEGER,
                signature TEXT,
                value TEXT,
                PRIMARY KEY (user_id, signature)
            )
            """
        )
        self.conn.commit()

    def get_facts(self, user_id: int) -> Dict[str, str]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT signature, value FROM facts WHERE user_id = ?",
            (user_id,)
        )

        rows = cursor.fetchall()
        return {row["signature"]: row["value"] for row in rows}

    def save_facts(self, user_id: int, facts: Dict[str, str]) -> None:
        cursor = self.conn.cursor()

        for signature, value in facts.items():
            cursor.execute(
                """
                INSERT OR REPLACE INTO facts (user_id, signature, value)
                VALUES (?, ?, ?)
                """,
                (user_id, signature, value)
            )

        self.conn.commit()

    def reset_user(self, user_id: int) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM facts WHERE user_id = ?",
            (user_id,)
        )
        self.conn.commit()


    def get_conversation(self, user_id: int):
        raise NotImplementedError()

    def save_conversation(self, user_id: int, messages):
        raise NotImplementedError()
