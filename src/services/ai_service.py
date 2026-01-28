import re
from openai import AsyncOpenAI
from src.infra.rate_limiter import RateLimiter
from src.memory.memory_store import MemoryStore


class AiService:
    def __init__(self, memory_store: MemoryStore):
        self.client = AsyncOpenAI()
        self.rate_limiter = RateLimiter(max_calls=5, window_seconds=60)
        self.memory_store = memory_store
        self.conversation_memory: dict[int, list[dict]] = {}

    async def ask(self, user_id: int, user_message: str) -> str:
        self.rate_limiter.check(user_id)
        history = self.memory_store.get_conversation(user_id)
        user_facts = self.memory_store.get_facts(user_id)

        facts_block = "\n".join(f"- {fact}" for fact in user_facts.values())

        messages = [
            {
                "role": "system",
                "content": (
                    "Jesteś miłym, wspierającym i pomocnym kolegą.\n"
                    "Poniżej znajdują się ZNANE FAKTY o użytkowniku.\n"
                    "Traktuj je jako prawdziwe i używaj ich w odpowiedziach.\n\n"
                    f"{facts_block if facts_block else 'Brak zapisanych faktów.'}"
                )
            },
            *history,
            {
                "role": "user",
                "content": user_message
            }
        ]
        response = await self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages
        )

        reply = response.choices[0].message.content or ""

        extracted_facts = await self.extract_facts(user_message)
        if extracted_facts:
            updated_facts = dict(user_facts)

            for fact in extracted_facts:
                clean_fact = self._clean_fact(fact)
                signature = self._fact_signature(clean_fact)
                updated_facts[signature] = clean_fact  # last-write-wins

            self.memory_store.save_facts(user_id, updated_facts)

        self.memory_store.save_conversation(
            user_id,
            [
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": reply}
            ]
        )
        return reply

    async def extract_facts(self, text: str) -> list[str]:
        response = await self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Wyciągnij z tekstu trwałe fakty o użytkowniku. "
                        "Zwróć każde jako osobne krótkie zdanie. "
                        "Jeśli nie ma faktów, zwróć pustą listę. "
                        "Nie wymyślaj nic."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        raw = (response.choices[0].message.content or "").strip()
        if not raw:
            return []

        return [line.strip("-• ").strip() for line in raw.split("\n") if line.strip()]

    def reset_user(self, user_id: int) -> None:
        self.conversation_memory.pop(user_id, None)
        self.memory_store.reset_user(user_id)

    def _fact_signature(self, fact: str) -> str:
        """
        Normalizuje fakt do logicznego klucza:
        'Użytkownik ma 23 lata.' -> 'użytkownik ma _ lata.'
        """
        fact = fact.lower()
        return re.sub(r"\d+", "_", fact)

    def _clean_fact(self, fact: str) -> str:
        """
        Czyści noisy output LLM (listy, cudzysłowy itp.)
        """
        fact = fact.strip()

        if fact.startswith("[") and fact.endswith("]"):
            fact = fact.strip("[]").strip()

        if fact.startswith('"') and fact.endswith('"'):
            fact = fact.strip('"')

        return fact