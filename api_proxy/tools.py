from aiohttp.web_request import Request


def build_headers(request: Request):
    headers = request.headers
    new_headers = dict(headers)
    new_user_agent = f"{headers['User-Agent']}/SyncWrapperAPI"
    new_headers['User-Agent'] = new_user_agent
    return new_headers
