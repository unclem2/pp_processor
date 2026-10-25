import asyncio
import time
from collections import deque


class AsyncRateLimiter:
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._timestamps: deque[float] = deque()
        self._lock = asyncio.Lock()

    async def try_acquire(self) -> bool:
        """Non-blocking acquire. Returns True if a slot was available, False if rate-limited."""
        async with self._lock:
            now = time.monotonic()
            while self._timestamps and now - self._timestamps[0] >= self.window_seconds:
                self._timestamps.popleft()

            if len(self._timestamps) >= self.max_requests:
                return False

            self._timestamps.append(now)
            return True

    async def acquire(self) -> None:
        """Backward-compatible acquire. Raises RateLimitExceeded if bucket is full."""
        if not await self.try_acquire():
            raise RateLimitExceeded()

    async def peek(self) -> tuple[int, float]:
        # Non-consuming view of the window.
        # Returns (free_slots, seconds_until_a_slot_frees_up).
        async with self._lock:
            now = time.monotonic()
            while self._timestamps and now - self._timestamps[0] >= self.window_seconds:
                self._timestamps.popleft()

            remaining = self.max_requests - len(self._timestamps)
            if self._timestamps:
                reset_in = self._timestamps[0] + self.window_seconds - now
            else:
                reset_in = self.window_seconds
            return remaining, reset_in


class RateLimitExceeded(Exception):
    pass
