import pytest


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
