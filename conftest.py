import pytest

from api.auth_api import create_token
from api.booking_api import create_booking, delete_booking
from config.secret_config import BASE_URL


@pytest.fixture(scope="session")
def auth_token(request_context):
    r = create_token(request_context)
    return r.json()["token"]


@pytest.fixture(scope="session")
def request_context(playwright):
    context = playwright.request.new_context(base_url=BASE_URL)
    yield context
    context.dispose()


@pytest.fixture
def api_headers():
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


@pytest.fixture
def api_headers_with_cookie():
    def _api_headers_with_cookie(token):
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f"token={token}"
        }

    return _api_headers_with_cookie
