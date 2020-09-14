import pytest
from aiohttp import web, ClientResponseError

from api_proxy.server.routes import setup_routes


async def hello(request):
    return web.Response(body=b'Hello, world')


@pytest.fixture
def translate_data():
    return {"context": {"from": "en", "to": "es",
                        "text": "API economy (application programming interface economy) is a general term that describes the way application programming interfaces (APIs) can positively affect an organization's profitability. An API is a customer interface for technology products that allows software components to communicate.kjkjhkhkjh"},
            "service": {"provider": "ai.text.translate.deepl.api"}}


def create_app(loop):
    app = web.Application(loop=loop)
    setup_routes(app=app)
    return app


async def test_index(aiohttp_client):
    client = await aiohttp_client(create_app)

    resp = await client.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert 'Hello Aiohttp!' in text


async def test_post__weird_url(aiohttp_client, translate_data):
    client = await aiohttp_client(create_app)
    with pytest.raises(ClientResponseError) as err_context:
        resp = await client.post('/olol/pika', data=translate_data)

    assert err_context.value.status == 400


async def test_post__translate_sync(aiohttp_client, translate_data):
    client = await aiohttp_client(create_app)
    resp = await client.post('/ai/text/translate', data=translate_data)

    assert resp.status == 200
    text = await resp.text()
    assert '/ai/text/translate' == text
