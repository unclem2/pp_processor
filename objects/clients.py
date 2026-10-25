import logging
from functools import wraps

from fastapi import HTTPException, status
from ossapi import OssapiAsync

from objects.rate_limiter import AsyncRateLimiter, RateLimitExceeded

logger = logging.getLogger(__name__)


class RateLimitedOssapiAsync:
    def __init__(self, client: OssapiAsync, rate_limiter: AsyncRateLimiter):
        self._client = client
        self._rate_limiter = rate_limiter

    def __getattr__(self, name: str):
        attr = getattr(self._client, name)
        if callable(attr):
            @wraps(attr)
            async def wrapper(*args, **kwargs):
                if not await self._rate_limiter.try_acquire():
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="osu! API rate limit exceeded, try again later",
                    )
                logger.debug("osu! API call: %s", name)
                return await attr(*args, **kwargs)
            return wrapper
        return attr