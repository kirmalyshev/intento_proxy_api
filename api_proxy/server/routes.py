from aiohttp.web_routedef import UrlDispatcher

from api_proxy.server.views import index, proxy


def setup_routes(app):
    router: UrlDispatcher = app.router

    router.add_route('*', '/', index, name='index')
    router.add_route('*', '/{url:.+}', proxy, name='proxy')
