import json
import logging

from aiohttp import ClientSession, ClientResponse
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from api_proxy.settings import get_config, PROXY_HOST, OPERATIONS_PATH


def build_headers(request: Request) -> dict:
    headers = request.headers
    new_headers = dict(headers)
    new_user_agent = f"{headers.get('User-Agent')}/SyncWrapperAPI"
    new_headers['User-Agent'] = new_user_agent

    # big scratch to avoid 504 from intento API
    host = new_headers.pop('Host', None)
    accept = new_headers.pop('Accept', None)
    lenght = new_headers.pop('Content-Length', None)
    return new_headers


async def get_post_data(request):
    if not await request.post():
        return
    data = await request.json()
    data = dict(data.items())
    logging.debug(f"post_data: {data}")
    return data


async def is_async_request(request: Request) -> bool:
    data = await get_post_data(request)
    if not data:
        return False
    service = data.get('service')
    if service and service.get("async", False):
        return True
    return False


async def proxy_sync_request(request: Request) -> Response:
    config = await get_config()
    method = request.method.lower()
    # print(f"content: {content}")

    new_host = config[PROXY_HOST]
    new_url = f'{new_host}{request.path}'
    new_headers = build_headers(request)
    # print(f"new_headers: {new_headers}")
    post_data = await get_post_data(request)

    async with ClientSession(headers=new_headers) as session:
        async with session.request(
                method, new_url, json=post_data
        ) as resp:
            text = await resp.text()
            return Response(text=text, content_type=new_headers.get('Content-Type'))


async def request_job_result(job_id, session) -> ClientResponse:
    config = await get_config()
    proxy_host = config[PROXY_HOST]
    new_url = f'{proxy_host}{config[OPERATIONS_PATH]}/{job_id}'
    # print(f"new_url: {new_url}")
    resp = await session.get(new_url)
    resp_json = json.loads(await resp.text())

    if resp_json["done"] is True:
        return resp

    return await request_job_result(job_id, session)


async def proxy_async_translate_request(request: Request):
    sync_response = await proxy_sync_request(request)
    resp_json = json.loads(sync_response.text)
    is_job_id = "id" in resp_json
    if not is_job_id:
        return sync_response

    job_id = resp_json["id"]

    new_headers = build_headers(request)

    async with ClientSession(headers=new_headers, conn_timeout=120) as session:
        response = await request_job_result(job_id, session)
        return Response(text=await response.text())
