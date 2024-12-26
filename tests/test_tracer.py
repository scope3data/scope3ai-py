import pytest


def test_tracer_linear():
    from scope3ai.api.tracer import Tracer, ModeledRow, ImpactMetrics

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


def test_tracer_nested():
    from scope3ai.api.tracer import Tracer, ModeledRow, ImpactMetrics

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
