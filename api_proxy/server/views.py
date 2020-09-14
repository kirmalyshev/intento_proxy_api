from aiohttp import ClientSession
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from api_proxy.settings import get_config, TRANSLATE_URL, PROXY_HOST
from api_proxy.tools import build_headers


async def index(request: Request) -> Response:
    return Response(text='Hello Aiohttp!')


async def proxy(request: Request) -> Response:
    url = request.match_info['url']
    path = request.path
    method = request.method
    content = request.can_read_body and request.content
    headers = request.headers
    print(f"headers: {headers}\n{content}\nmethod:{method}")
    config = await get_config()

    if path != config[TRANSLATE_URL]:
        return await run_sync_request(request)

    params = request.query
    is_async = params.get('async', False)
    print(is_async, '---')
    is_async = bool(is_async)
    if not is_async:
        return await run_sync_request(request)
    else:
        return Response(text=f"{path}")


async def run_sync_request(request: Request) -> Response:
    config = await get_config()

    method = request.method.lower()
    content = request.can_read_body and request.content

    new_host = config[PROXY_HOST]
    new_url = f'{new_host}{request.path}'
    new_headers = build_headers(request)

    async with ClientSession() as session:
        async with session.request(
                method, new_url, headers=new_headers, data=content
        ) as resp:
            text = await resp.text()
            # json = await resp.json()
            return Response(text=text, content_type=new_headers['Content-Type'])
