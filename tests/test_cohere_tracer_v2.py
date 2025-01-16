import pytest
from cohere import ClientV2, AsyncClientV2


@pytest.mark.vcr
def test_cohere_chat_v2(tracer_with_sync_init):
    client = ClientV2()
    response = client.chat(
        model="command-r-plus-08-2024",
        messages=[{"role": "user", "content": "Hello world!"}],
    )
    assert len(response.message.content) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 204
    assert response.scope3ai.request.output_tokens == 9
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_cohere_async_chat_v2(tracer_with_sync_init):
    client = AsyncClientV2()
    response = await client.chat(
        model="command-r-plus-08-2024",
        messages=[{"role": "user", "content": "Hello world!"}],
    )
    assert len(response.message.content) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 204
    assert response.scope3ai.request.output_tokens == 9
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_cohere_stream_chat_v2(tracer_with_sync_init):
    client = ClientV2()
    stream = client.chat_stream(
        model="command-r-plus-08-2024",
        messages=[{"role": "user", "content": "Tell me a short story"}],
        max_tokens=100,
    )
    event_received = False
    for event in stream:
        if event.type == "text-generation":
            assert len(event.text) > 0
        if event.type == "scope3ai":
            assert getattr(event, "scope3ai") is not None
            assert event.scope3ai.request.input_tokens == 206
            assert event.scope3ai.request.output_tokens == 100
            assert event.scope3ai.impact is not None
            assert event.scope3ai.impact.total_impact is not None
            assert event.scope3ai.impact.total_impact.usage_energy_wh > 0
            assert event.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
            assert event.scope3ai.impact.total_impact.usage_water_ml > 0
            assert event.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
            assert event.scope3ai.impact.total_impact.embodied_water_ml > 0
            event_received = True

    assert event_received is True


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_cohere_async_stream_chat_v2(tracer_with_sync_init):
    client = AsyncClientV2()
    stream = client.chat_stream(
        model="command-r-plus-08-2024",
        messages=[{"role": "user", "content": "Tell me a short story"}],
        max_tokens=100,
    )
    event_received = False
    async for event in stream:
        if event.type == "text-generation":
            assert len(event.text) > 0
        if event.type == "scope3ai":
            assert getattr(event, "scope3ai") is not None
            assert event.scope3ai.request.input_tokens == 206
            assert event.scope3ai.request.output_tokens == 100
            assert event.scope3ai.impact is not None
            assert event.scope3ai.impact.total_impact is not None
            assert event.scope3ai.impact.total_impact.usage_energy_wh > 0
            assert event.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
            assert event.scope3ai.impact.total_impact.usage_water_ml > 0
            assert event.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
            assert event.scope3ai.impact.total_impact.embodied_water_ml > 0
            event_received = True

    assert event_received is True
