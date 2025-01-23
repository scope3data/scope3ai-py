from typing import Optional

import pytest


def test_lib_init_default():
    from scope3ai import Scope3AI

    scope3: Optional[Scope3AI] = None
    try:
        scope3 = Scope3AI.init(api_key="dummy", providers=[])
        assert scope3.environment is None
        assert scope3.application_id == "default"
        assert scope3.client_id is None
        assert scope3.project_id is None
    finally:
        if scope3:
            scope3.close()


@pytest.fixture
def init_env():
    import os

    os.environ["SCOPE3AI_ENVIRONMENT"] = "environment"
    os.environ["SCOPE3AI_APPLICATION_ID"] = "application_id"
    os.environ["SCOPE3AI_CLIENT_ID"] = "client_id"
    os.environ["SCOPE3AI_PROJECT_ID"] = "project_id"
    yield
    del os.environ["SCOPE3AI_ENVIRONMENT"]
    del os.environ["SCOPE3AI_APPLICATION_ID"]
    del os.environ["SCOPE3AI_CLIENT_ID"]
    del os.environ["SCOPE3AI_PROJECT_ID"]


def test_lib_init_env(init_env):
    from scope3ai import Scope3AI

    scope3: Optional[Scope3AI] = None
    try:
        scope3 = Scope3AI.init(api_key="dummy", providers=[])
        assert scope3.environment == "environment"
        assert scope3.application_id == "application_id"
        assert scope3.client_id == "client_id"
        assert scope3.project_id == "project_id"
    finally:
        if scope3:
            scope3.close()


def test_lib_init_precedence(init_env):
    from scope3ai import Scope3AI

    scope3: Optional[Scope3AI] = None
    try:
        scope3 = Scope3AI.init(
            api_key="dummy",
            environment="environment_2",
            application_id="application_id_2",
            client_id="client_id_2",
            project_id="project_id_2",
            providers=[],
        )
        assert scope3.environment == "environment_2"
        assert scope3.application_id == "application_id_2"
        assert scope3.client_id == "client_id_2"
        assert scope3.project_id == "project_id_2"
    finally:
        if scope3:
            scope3.close()


def test_impact_row_no_tracer(init_env, tracer_init):
    from scope3ai.api.types import ImpactRow

    # pause the background worker
    tracer_init._ensure_worker()
    tracer_init._worker.pause()

    impact = ImpactRow(model_id="gpt_4o", input_tokens=100, output_tokens=100)
    ctx = tracer_init.submit_impact(impact)
    request = ctx.request
    assert request.utc_datetime is not None
    assert request.request_id is not None
    assert request.trace_id is None
    assert request.session_id is None
    assert request.environment == "environment"
    assert request.application_id == "application_id"
    assert request.client_id == "client_id"
    assert request.project_id == "project_id"

    tracer_init._worker.resume()


def test_impact_row_with_tracer(init_env, tracer_init):
    from scope3ai.api.types import ImpactRow

    # pause the background worker
    tracer_init._ensure_worker()
    tracer_init._worker.pause()

    with tracer_init.trace(
        application_id="application_id_2",
        client_id="client_id_2",
        project_id="project_id_2",
    ) as tracer:
        impact = ImpactRow(model_id="gpt_4o", input_tokens=100, output_tokens=100)
        ctx = tracer_init.submit_impact(impact)
        request = ctx.request
        assert request.utc_datetime is not None
        assert request.request_id is not None
        assert request.session_id is None
        assert request.trace_id == tracer.trace_id
        assert request.environment == "environment"
        assert request.application_id == "application_id_2"
        assert request.client_id == "client_id_2"
        assert request.project_id == "project_id_2"

    tracer_init._worker.resume()


def test_impact_row_with_nested_tracer(init_env, tracer_init):
    from scope3ai.api.types import ImpactRow

    # pause the background worker
    tracer_init._ensure_worker()
    tracer_init._worker.pause()

    with tracer_init.trace(
        application_id="application_id_2",
        client_id="client_id_2",
    ) as root_tracer:
        with tracer_init.trace(
            project_id="project_id_3",
        ):
            impact = ImpactRow(model_id="gpt_4o", input_tokens=100, output_tokens=100)
            ctx = tracer_init.submit_impact(impact)
            request = ctx.request
            assert request.utc_datetime is not None
            assert request.request_id is not None
            assert request.session_id is None
            assert request.trace_id == root_tracer.trace_id
            assert request.environment == "environment"
            assert request.application_id == "application_id_2"
            assert request.client_id == "client_id_2"
            assert request.project_id == "project_id_3"

    tracer_init._worker.resume()


def test_impact_row_with_session_id(tracer_init):
    from scope3ai.api.types import ImpactRow

    # pause the background worker
    tracer_init._ensure_worker()
    tracer_init._worker.pause()

    with tracer_init.trace(
        session_id="session_id_1",
    ) as tracer:
        impact = ImpactRow(model_id="gpt_4o", input_tokens=100, output_tokens=100)
        ctx = tracer_init.submit_impact(impact)
        request = ctx.request
        assert request.utc_datetime is not None
        assert request.request_id is not None
        assert request.trace_id == tracer.trace_id
        assert request.session_id == "session_id_1"

    tracer_init._worker.resume()


def test_impact_row_nested_with_session_id(tracer_init):
    from scope3ai.api.types import ImpactRow

    # pause the background worker
    tracer_init._ensure_worker()
    tracer_init._worker.pause()

    with tracer_init.trace(
        session_id="session_id_1",
    ) as tracer:
        with tracer_init.trace(
            session_id="session_id_2",
        ):
            impact = ImpactRow(model_id="gpt_4o", input_tokens=100, output_tokens=100)
            ctx = tracer_init.submit_impact(impact)
            request = ctx.request
            assert request.utc_datetime is not None
            assert request.request_id is not None
            assert request.trace_id == tracer.trace_id
            assert request.session_id == "session_id_2"

    tracer_init._worker.resume()
