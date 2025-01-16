import pytest
from cohere import Client, AsyncClient


@pytest.mark.vcr
def test_cohere_chat(tracer_with_sync_init):
    client = Client()
    response = client.chat(message="Hello!", max_tokens=100)
    assert len(response.text) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 203
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
async def test_cohere_async_chat(tracer_with_sync_init):
    client = AsyncClient()
    response = await client.chat(message="Hello!", max_tokens=100)
    assert len(response.text) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 203
    assert response.scope3ai.request.output_tokens == 9
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_cohere_stream_chat(tracer_with_sync_init):
    client = Client()
    stream = client.chat_stream(message="Tell me a short story", max_tokens=100)
    for event in stream:
        if event.event_type == "text-generation":
            assert len(event.text) > 0
        if event.event_type == "stream-end":
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


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_cohere_async_stream_chat(tracer_with_sync_init):
    client = AsyncClient()
    stream = client.chat_stream(message="Tell me a short story", max_tokens=100)
    async for event in stream:
        if event.event_type == "text-generation":
            assert len(event.text) > 0
        if event.event_type == "stream-end":
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
