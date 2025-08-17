
import pytest


from core.clients.api_client import APIClient


@pytest.fixture(scope='session')
def api_client():
    client = APIClient()
    return client