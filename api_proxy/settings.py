import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / 'config' / 'polls.yaml'


TRANSLATE_URL = "translate_url"
PROXY_HOST = "proxy_host"


async def get_config(argv=None) -> dict:
    data = {
        TRANSLATE_URL: os.getenv('TRANSLATE_URL'),
        PROXY_HOST: os.getenv('PROXY_HOST'),
    }
    return data
