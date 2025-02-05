import pytest


def test_tracer_linear(tracer_init):
    from scope3ai.api.tracer import Tracer
    from scope3ai.api.types import ModeledRow, ImpactMetrics

    tracer = Tracer()
    assert tracer is not None

    metric = ImpactMetrics(
        usage_energy_wh=1,
        usage_emissions_gco2e=2,
        usage_water_ml=3,
        embodied_emissions_gco2e=4,
        embodied_water_ml=5,
    )
    row = ModeledRow(inference_impact=metric, total_impact=metric)

    # try with one row

    tracer.add_impact(row)
    response = tracer.impact()
    assert len(response.rows) == 1
    assert response.total_energy_wh == 1
    assert response.total_gco2e == 2
    assert response.total_mlh2o == 3

    # try with two rows, ensure the total is correct

    tracer.add_impact(row)
    response = tracer.impact()
    assert len(response.rows) == 2
    assert response.total_energy_wh == 2
    assert response.total_gco2e == 4
    assert response.total_mlh2o == 6


def test_tracer_nested(tracer_init):
    from scope3ai.api.tracer import Tracer
    from scope3ai.api.types import ModeledRow, ImpactMetrics

    tracer = Tracer()
    tracer2 = Tracer()
    assert tracer is not None

    metric = ImpactMetrics(
        usage_energy_wh=1,
        usage_emissions_gco2e=1,
        usage_water_ml=1,
        embodied_emissions_gco2e=1,
        embodied_water_ml=1,
    )
    metric2 = ImpactMetrics(
        usage_energy_wh=2,
        usage_emissions_gco2e=2,
        usage_water_ml=2,
        embodied_emissions_gco2e=2,
        embodied_water_ml=2,
    )
    row = ModeledRow(inference_impact=metric, total_impact=metric)
    row2 = ModeledRow(training_impact=metric2, total_impact=metric2)

    tracer.add_impact(row)
    tracer2.add_impact(row2)
    tracer2.add_impact(row2)
    tracer2._link_parent(tracer)

    # ensure tracer2 is a child of tracer
    assert tracer2 in tracer.children

    # check that tracer have global impact
    response = tracer.impact()
    assert len(response.rows) == 3  # does contains the row from tracer2
    assert response.total_energy_wh == 5
    assert response.total_gco2e == 5
    assert response.total_mlh2o == 5

    # check that tracer2 have not impact from tracer
    response = tracer2.impact()
    assert len(response.rows) == 2
    assert response.total_energy_wh == 4
    assert response.total_gco2e == 4
    assert response.total_mlh2o == 4


@pytest.mark.vcr
def test_tracer_openai_simple_synchronisation(tracer_init):
    from openai import OpenAI

    # pause the background worker
    tracer_init._ensure_worker()
    tracer_init._worker.pause()

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4", messages=[{"role": "user", "content": "Hello World!"}]
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 10
    assert response.scope3ai.request.output_tokens == 10
    assert response.scope3ai.impact is None

    # should raise a timeout error because the worker is paused
    with pytest.raises(TimeoutError):
        response.scope3ai.wait_impact(timeout=1)

    # now unpause the worker
    tracer_init._worker.resume()
    response.scope3ai.wait_impact()
    assert response.scope3ai.impact is not None


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_tracer_openai_simple_asynchronisation(tracer_init):
    import asyncio
    from openai import AsyncOpenAI

    # pause the background worker
    tracer_init._ensure_worker()
    tracer_init._worker.pause()

    client = AsyncOpenAI()
    response = await client.chat.completions.create(
        model="gpt-4", messages=[{"role": "user", "content": "Hello World!"}]
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 10
    assert response.scope3ai.request.output_tokens == 10
    assert response.scope3ai.impact is None

    # should raise a timeout error because the worker is paused
    with pytest.raises(asyncio.TimeoutError):
        await response.scope3ai.await_impact(timeout=1)

    # now unpause the worker
    tracer_init._worker.resume()
    await response.scope3ai.await_impact()
    assert response.scope3ai.impact is not None


@pytest.mark.vcr
def test_tracer_context(tracer_init):
    from openai import OpenAI

    client = OpenAI()
    with tracer_init.trace() as tracer:
        response = client.chat.completions.create(
            model="gpt-4", messages=[{"role": "user", "content": "Hello World!"}]
        )
        assert len(response.choices) > 0
        impact = tracer.impact()
        assert impact is not None
        assert impact.total_energy_wh > 0
        assert impact.total_gco2e > 0
        assert impact.total_mlh2o > 0


@pytest.mark.vcr
def test_tracer_context_nested(tracer_init):
    from openai import OpenAI

    client = OpenAI()
    with tracer_init.trace() as tracer:
        response = client.chat.completions.create(
            model="gpt-4", messages=[{"role": "user", "content": "Hello World!"}]
        )
        assert len(response.choices) > 0

        with tracer_init.trace() as tracer2:
            response = client.chat.completions.create(
                model="gpt-4", messages=[{"role": "user", "content": "Hello World!"}]
            )
            assert len(response.choices) > 0
            impact = tracer2.impact()
            assert impact is not None
            assert impact.total_energy_wh > 0
            assert impact.total_gco2e > 0
            assert impact.total_mlh2o > 0

        impact2 = tracer.impact()
        assert impact2 is not None
        assert impact2.total_energy_wh > impact.total_energy_wh
        assert impact2.total_gco2e > impact.total_gco2e
        assert impact2.total_mlh2o > impact.total_mlh2o


@pytest.mark.vcr
def test_tracer_rows(tracer_init):
    from mistralai import Mistral
    import os

    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

    with tracer_init.trace() as tracer:
        client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {
                    "role": "user",
                    "content": "Give me small summary of 100 years of Loneliness",
                }
            ],
            max_tokens=100,
            temperature=0.7,
        )

        impact = tracer.impact()
        assert impact is not None
        assert impact.total_energy_wh > 0
        assert impact.total_gco2e > 0
        assert impact.total_mlh2o > 0
        assert len(tracer.get_all_rows()) == 1


def test_tracer_submit_impact(tracer_init):
    from scope3ai.api.types import ImpactRow

    # pause the background worker
    tracer_init._ensure_worker()
    tracer_init._worker.pause()

    impact = ImpactRow(model_id="gpt_4o", input_tokens=100, output_tokens=100)
    ctx = tracer_init.submit_impact(impact)

    assert ctx is not None
    assert ctx.impact is None

    # resume the background worker
    tracer_init._worker.resume()

    ctx.wait_impact()
    assert ctx.impact is not None


def test_tracer_submit_impact_sync(tracer_with_sync_init):
    from scope3ai.api.types import ImpactRow

    impact = ImpactRow(model_id="gpt_4o", input_tokens=100, output_tokens=100)
    ctx = tracer_with_sync_init.submit_impact(impact)

    assert ctx is not None
    assert ctx.impact is not None


@pytest.mark.asyncio
async def test_tracer_submit_impact_async(tracer_init):
    from scope3ai.api.types import ImpactRow

    # pause the background worker
    tracer_init._ensure_worker()
    tracer_init._worker.pause()

    impact = ImpactRow(model_id="gpt_4o", input_tokens=100, output_tokens=100)
    ctx = await tracer_init.asubmit_impact(impact)

    assert ctx is not None
    assert ctx.impact is None

    # resume the background worker
    tracer_init._worker.resume()
    await ctx.await_impact()
    assert ctx.impact is not None


@pytest.mark.asyncio
async def test_tracer_submit_impact_sync_async(tracer_with_sync_init):
    from scope3ai.api.types import ImpactRow

    impact = ImpactRow(model_id="gpt_4o", input_tokens=100, output_tokens=100)
    ctx = await tracer_with_sync_init.asubmit_impact(impact)

    assert ctx is not None
    assert ctx.impact is not None
