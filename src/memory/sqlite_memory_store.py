import sqlite3
from typing import Dict
from src.memory.memory_store import MemoryStore
import time

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
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS conversation (
                user_id INTEGER,
                role TEXT,
                content TEXT,
                created_at INTEGER
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
        cursor.execute("DELETE FROM facts WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM conversation WHERE user_id = ?", (user_id,))
        self.conn.commit()

    def get_conversation(self, user_id: int, limit: int = 10):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT role, content
            FROM conversation
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit)
        )
        rows = cursor.fetchall()
        rows.reverse()
        return [{"role": row["role"], "content": row["content"]} for row in rows]

    def save_conversation(self, user_id: int, messages):
        cursor = self.conn.cursor()
        timestamp = int(time.time())
        for message in messages:
            cursor.execute(
                """
                INSERT INTO conversation (user_id, role, content, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, message["role"], message["content"], timestamp)
            )
        self.conn.commit()
