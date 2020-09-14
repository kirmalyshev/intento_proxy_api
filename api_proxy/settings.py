import os
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / 'config' / 'polls.yaml'


PROXY_HOST = "proxy_host"
TRANSLATE_PATH = "translate_url"
OPERATIONS_PATH = "operations_path"


async def get_config(argv=None) -> dict:
    data = {
        PROXY_HOST: os.getenv('PROXY_HOST'),
        TRANSLATE_PATH: os.getenv('TRANSLATE_PATH'),
        OPERATIONS_PATH: os.getenv('OPERATIONS_PATH'),
    }
    if not all(data.values()):
        raise ValueError("not all of config variables are set")
    return data
