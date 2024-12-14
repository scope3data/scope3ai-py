import pytest


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": [("authorization", "DUMMY")],
        "ignore_localhost": True,
        "ignore_hosts": ["aiapi.scope3.com"],
    }


@pytest.fixture
def tracer_init():
    from scope3ai import Scope3AI

    scope3 = Scope3AI.init(enable_debug_logging=True)
    try:
        yield scope3
    finally:
        scope3.close()


@pytest.fixture
def tracer_with_response_init():
    from scope3ai import Scope3AI

    scope3 = Scope3AI.init(
        enable_debug_logging=True,
        include_impact_response=True,
    )
    try:
        yield scope3
    finally:
        scope3.close()
