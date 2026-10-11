import asyncio
import time
from collections import deque


class AsyncRateLimiter:
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._timestamps: deque[float] = deque()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            while self._timestamps and now - self._timestamps[0] >= self.window_seconds:
                self._timestamps.popleft()

            if len(self._timestamps) >= self.max_requests:
                sleep_until = self._timestamps[0] + self.window_seconds
                sleep_duration = sleep_until - now
                if sleep_duration > 0:
                    await asyncio.sleep(sleep_duration)
                self._timestamps.popleft()

            self._timestamps.append(time.monotonic())