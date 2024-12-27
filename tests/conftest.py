import os
import pytest
import httpx
from pytest_docker.plugin import containers_scope


def set_envvar_if_unset(name: str, value: str):
    if os.getenv(name) is None:
        os.environ[name] = value


@pytest.fixture(autouse=True)
def environment():
    set_envvar_if_unset("ANTHROPIC_API_KEY", "DUMMY")
    set_envvar_if_unset("COHERE_API_KEY", "DUMMY")
    set_envvar_if_unset("OPENAI_API_KEY", "DUMMY")


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": [("authorization", "DUMMY"), ("x-api-key", "DUMMY")],
        "ignore_localhost": True,
        "ignore_hosts": ["aiapi.scope3.com"],
    }


def is_responsive(url):
    try:
        response = httpx.get(url)
        return response.status_code == 405  # Method not allowed
    except (httpx.RequestError, httpx.HTTPStatusError):
        return False


@pytest.fixture(scope="session")
def docker_api_info(docker_ip, docker_services):
    port = docker_services.port_for("prism", 4010)
    url = f"http://{docker_ip}:{port}"
    docker_services.wait_until_responsive(
        timeout=30.0,
        pause=0.1,
        check=lambda: is_responsive(url),
    )
    return {
        "api_key": "DUMMY",
        "api_url": url,
    }


@pytest.fixture(scope=containers_scope)
def docker_cleanup():
    # faster cleanup than waiting node to exit
    return ["exec prism pkill -TERM node", "down -v"]


@pytest.fixture
def tracer_init(docker_api_info):
    from scope3ai import Scope3AI

    scope3 = Scope3AI.init(enable_debug_logging=True, **docker_api_info)
    try:
        yield scope3
    finally:
        scope3.close()


@pytest.fixture
def tracer_with_response_init(docker_api_info):
    from scope3ai import Scope3AI

    scope3 = Scope3AI.init(
        enable_debug_logging=True,
        sync_mode=True,
        **docker_api_info,
    )
    try:
        yield scope3
    finally:
        scope3.close()
