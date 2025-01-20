import os

import httpx
import pytest


def set_envvar_if_unset(name: str, value: str):
    if os.getenv(name) is None:
        os.environ[name] = value


@pytest.fixture(autouse=True)
def environment():
    set_envvar_if_unset("ANTHROPIC_API_KEY", "DUMMY")
    set_envvar_if_unset("COHERE_API_KEY", "DUMMY")
    set_envvar_if_unset("OPENAI_API_KEY", "DUMMY")
    set_envvar_if_unset("LITELLM_LOCAL_MODEL_COST_MAP", "True")


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


# @pytest.fixture(scope=containers_scope)
# def docker_cleanup():
#     # faster cleanup than waiting node to exit
#     return ["exec prism pkill -TERM node", "down -v"]


@pytest.fixture
def tracer_init(docker_api_info):
    from scope3ai import Scope3AI

    scope3 = Scope3AI.init(enable_debug_logging=True, **docker_api_info)
    try:
        yield scope3
    finally:
        scope3.close()


@pytest.fixture
def tracer_with_sync_init(docker_api_info):
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


@pytest.fixture
def api_client(docker_api_info):
    from scope3ai.api.client import Client

    yield Client(
        api_key=docker_api_info["api_key"],
        api_url=docker_api_info["api_url"],
    )


@pytest.fixture
def async_api_client(docker_api_info):
    from scope3ai.api.client import AsyncClient

    yield AsyncClient(
        api_key=docker_api_info["api_key"],
        api_url=docker_api_info["api_url"],
    )


@pytest.fixture(autouse=True)
def fix_vcr_binary_utf8_decoding():
    # this handle httpx UTF-8 decoding issue
    # https://github.com/kevin1024/vcrpy/pull/882

    import warnings

    import vcr  # type: ignore[import-untyped]
    import vcr.stubs.httpx_stubs
    from vcr.request import Request as VcrRequest  # type: ignore[import-untyped]
    from vcr.stubs.httpx_stubs import (  # type: ignore
        _make_vcr_request,  # noqa: F401 this is needed for some reason so python knows this method exists
    )

    def _fixed__make_vcr_request(  # type: ignore
        httpx_request,
        **kwargs,  # noqa: ARG001
    ) -> VcrRequest:
        try:
            body = httpx_request.read().decode("utf-8")
        except UnicodeDecodeError as e:  # noqa: F841
            body = httpx_request.read().decode("utf-8", errors="ignore")
            warnings.warn(
                f"Could not decode full request payload as UTF8, recording may have lost bytes. {e}",
                stacklevel=2,
            )
        uri = str(httpx_request.url)
        headers = dict(httpx_request.headers)
        return VcrRequest(httpx_request.method, uri, body, headers)

    vcr.stubs.httpx_stubs._make_vcr_request = _fixed__make_vcr_request
    yield
    vcr.stubs.httpx_stubs._make_vcr_request = _make_vcr_request


@pytest.fixture(autouse=True)
def fix_vcr_body_read_missing_seek():
    # if the body is a file or bufferedio with aiohttp used
    # the body will be read by the vcr.Request, and the next body.read()
    # done by aiohttp will be empty.
    # IMO it is missing a seek(0) in the vcr.Request constructor after the read()
    import vcr.request

    request_init_orig = vcr.request.Request.__init__

    def _fixed__request_init(self, method, uri, body, headers):
        request_init_orig(self, method, uri, body, headers)
        if self._was_file:
            body.seek(0)

    vcr.request.Request.__init__ = _fixed__request_init
    yield
    vcr.request.Request.__init__ = request_init_orig
