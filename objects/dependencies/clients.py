from fastapi import Request

from objects.clients import RateLimitedOssapiAsync


async def get_osuapi_client(request: Request) -> RateLimitedOssapiAsync:
    return request.app.state.osuapi_client
