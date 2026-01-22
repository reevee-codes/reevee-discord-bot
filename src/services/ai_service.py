from openai import AsyncOpenAI
from src.infra.rate_limiter import RateLimiter


class AiService:
    def __init__(self):
        self.client = AsyncOpenAI()
        self.rate_limiter = RateLimiter(max_calls=5, window_seconds=60)
        self.memory: dict[int, list[dict]] = {}
        self.facts: dict[int, dict[str, str]] = {}

    async def ask(self, user_id: int, user_message: str) -> str:
        self.rate_limiter.check(user_id)

        history = self.memory.get(user_id, [])

        user_facts = self.facts.get(user_id, {})
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
            user_facts = self.facts.setdefault(user_id, {})

            for fact in extracted_facts:
                key = self._normalize_fact(fact)
                user_facts[key] = fact

        self.memory[user_id] = (
            history
            + [
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": reply}
            ]
        )[-10:]

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

    def get_facts(self, user_id: int) -> list[str]:
        return list(self.facts.get(user_id, {}).values())

    def reset_user(self, user_id: int) -> None:
        self.memory.pop(user_id, None)
        self.facts.pop(user_id, None)

    def _normalize_fact(self, fact: str) -> str:
        return fact.strip().lower()
