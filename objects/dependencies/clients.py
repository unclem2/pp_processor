from fastapi import Request
from ossapi import OssapiAsync


async def get_osuapi_client(request: Request) -> OssapiAsync:
    return request.app.state.osuapi_client
