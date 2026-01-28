from abc import ABC, abstractmethod
from typing import List, Dict

class MemoryStore(ABC):

    @abstractmethod
    def get_conversation(self, user_id: int) -> List[Dict]:
        pass

    @abstractmethod
    def save_conversation(self, user_id: int, messages: List[Dict]) -> None:
        pass

    @abstractmethod
    def get_facts(self, user_id: int) -> Dict[str, str]:
        pass

    @abstractmethod
    def save_facts(self, user_id: int, facts: Dict[str, str]) -> None:
        pass

    @abstractmethod
    def reset_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    def get_todo(self, user_id: int) -> List[str]:
        pass
