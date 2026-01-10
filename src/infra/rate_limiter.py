import time
from src.errors.command_error import CommandError

class RateLimiter:
    def __init__(self, max_calls: int, window_seconds: int):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls = {}

    def check(self, user_id: int):
        now = time.time()
        timestamps = self.calls.get(user_id, [])

        timestamps = [
            ts for ts in timestamps
            if now - ts < self.window_seconds
        ]

        if len(timestamps) >= self.max_calls:
            raise CommandError(
                f"Zwolnij trochę 🫶 Możesz użyć tej komendy "
                f"{self.max_calls} razy na {self.window_seconds} sekund."
            )

        timestamps.append(now)
        self.calls[user_id] = timestamps
