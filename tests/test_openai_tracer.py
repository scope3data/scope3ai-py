import pytest


@pytest.mark.vcr
def test_openai_chat(tracer_init):
    from openai import OpenAI

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4", messages=[{"role": "user", "content": "Hello World!"}]
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 10
    assert response.scope3ai.request.output_tokens == 9
    assert response.scope3ai.impact is None


@pytest.mark.vcr
def test_openai_chat_with_response(tracer_with_sync_init):
    from openai import OpenAI

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4", messages=[{"role": "user", "content": "Hello World!"}]
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 10
    assert response.scope3ai.request.output_tokens == 9
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0


@pytest.mark.vcr
def test_openai_chat_stream(tracer_init):
    from openai import OpenAI

    client = OpenAI()

    with tracer_init.trace() as tracer:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello World!"}],
            stream=True,
        )

        for event in response:
            if not event.choices:
                continue
            print(event.choices[0].delta.content, end="", flush=True)
        print()

        impact = tracer.impact()
        assert impact.total_energy_wh > 0
        assert impact.total_gco2e > 0
        assert impact.total_mlh2o > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_openai_chat_stream_async(tracer_init):
    from openai import AsyncOpenAI

    client = AsyncOpenAI()

    with tracer_init.trace() as tracer:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello World!"}],
            stream=True,
        )

        async for event in response:
            if not event.choices:
                continue
            print(event.choices[0].delta.content, end="", flush=True)
        print()

        impact = tracer.impact()
        assert impact.total_energy_wh > 0
        assert impact.total_gco2e > 0
        assert impact.total_mlh2o > 0
