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
                            "You are a kind, supportive, and helpful colleague."
                            "You respond calmly, empathetically, and without judgment."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )
        except Exception:
            raise CommandError("Problem with openAI connection")

        return response.choices[0].message.content