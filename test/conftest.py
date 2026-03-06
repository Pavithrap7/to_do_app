import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="http://localhost:8000",
        help="Base URL for API tests"
    )

@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url")
