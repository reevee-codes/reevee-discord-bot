from openai import AsyncOpenAI
from src.infra.rate_limiter import RateLimiter

class AiService:
    def __init__(self):
        self.client = AsyncOpenAI()
        self.memory = {}
        self.facts = {}
        self.rate_limiter = RateLimiter(max_calls = 5, window_seconds = 60)

    async def ask(self, user_id: int, user_message: str) -> str:
        self.rate_limiter.check(user_id)
        history = self.memory.get(user_id, [])
        facts = self.facts.get(user_id, [])
        facts_block = "\n".join(f"- {fact}" for fact in facts)

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

        reply = response.choices[0].message.content

        facts = await self.extract_facts(user_message)
        if facts:
            self.facts.setdefault(user_id, []).extend(facts)

        self.memory[user_id] = (
                history
                + [{"role": "user", "content": user_message},
                   {"role": "assistant", "content": reply}]
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
                        "Zwróć listę krótkich zdań albo pustą listę. "
                        "Nie wymyślaj nic"
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        raw = response.choices[0].message.content.strip()

        if not raw:
            return []

        return [line.strip("-• ") for line in raw.split("\n") if line.strip()]

    def get_facts(self, user_id: int) -> list[str]:
        return self.facts.get(user_id, [])