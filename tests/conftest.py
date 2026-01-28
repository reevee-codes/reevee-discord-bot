import sys
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.memory.sqlite_memory_store import SqliteMemoryStore


@pytest.fixture
def memory_store(tmp_path):
    db_path = tmp_path / "test_memory.db"
    return SqliteMemoryStore(db_path=db_path)
