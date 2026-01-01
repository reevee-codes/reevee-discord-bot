from openai import AsyncOpenAI
from errors.command_error import CommandError

class AiService:
    def __init__(self):
        self.client = AsyncOpenAI()

    async def ask(self, user_message: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Jesteś miłym, wspierającym i pomocnym kolegą. "
                            "Odpowiadasz spokojnie, empatycznie i bez oceniania."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )
        except Exception:
            raise CommandError("Nie udało się skontaktować z AI")

        return response.choices[0].message.content