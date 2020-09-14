from aiohttp.web_request import Request
from aiohttp.web_response import Response

from api_proxy.settings import get_config, TRANSLATE_PATH
from api_proxy.tools import is_async_request, proxy_sync_request, proxy_async_translate_request


async def index(request: Request) -> Response:
    return Response(text='Hello Aiohttp!')


async def proxy(request: Request) -> Response:
    path = request.path
    config = await get_config()

    if path != config[TRANSLATE_PATH]:
        return await proxy_sync_request(request)

    is_async = await is_async_request(request)

    if is_async:
        return await proxy_async_translate_request(request)
    else:
        return await proxy_sync_request(request)
