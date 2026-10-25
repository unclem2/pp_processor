import math
import time

from fastapi import HTTPException, Request, status

from objects.rate_limiter import AsyncRateLimiter

RATE_LIMIT_MARKER = "osu_rate_limited"


async def osu_api_rate_limit(request: Request) -> None:
    # The endpoint budget is the osu! API bucket itself: slots are spent only
    # by real API calls made through RateLimitedOssapiAsync. A request served
    # from the database never touches the bucket, so it is not counted.
    # This dependency marks the response for the header middleware and rejects
    # early once the shared bucket is exhausted, because such a request would
    # otherwise block waiting for API capacity.
    limiter: AsyncRateLimiter = request.app.state.osu_rate_limiter
    setattr(request.state, RATE_LIMIT_MARKER, True)

    remaining, reset_in = await limiter.peek()
    if remaining <= 0:
        retry_after = max(1, math.ceil(reset_in))
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="osu! API rate limit exceeded, try again later",
            headers={
                "X-RateLimit-Limit": str(limiter.max_requests),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(int(time.time()) + retry_after),
                "Retry-After": str(retry_after),
            },
        )
