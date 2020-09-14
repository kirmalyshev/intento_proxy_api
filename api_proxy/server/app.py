from aiohttp import web

from api_proxy.server.routes import setup_routes


def init_app() -> web.Application:
    web_app = web.Application()
    setup_routes(web_app)
    return web_app


app = init_app()
