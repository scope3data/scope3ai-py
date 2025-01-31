import pytest
from google.genai import Client
import os


@pytest.mark.vcr(decode_compressed_response=True)
def test_gemini_chat(tracer_with_sync_init):
    client = Client(api_key=os.environ["GOOGLE_API_KEY"])
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp", contents="How does RLHF work?"
    )
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.request_duration_ms > 0
    assert response.scope3ai.request.input_tokens > 0
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr(decode_compressed_response=True)
@pytest.mark.asyncio
async def test_gemini_chat_async(tracer_with_sync_init):
    client = Client(api_key=os.environ["GOOGLE_API_KEY"])
    response = await client.aio.models.generate_content(
        model="gemini-2.0-flash-exp", contents="How does RLHF work?"
    )
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.request_duration_ms > 0
    assert response.scope3ai.request.input_tokens > 0
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_gemini_chat_stream(tracer_with_sync_init):
    client = Client(api_key=os.environ["GOOGLE_API_KEY"])
    chat = client.chats.create(model="gemini-2.0-flash-exp")
    for chunk in chat.send_message_stream("tell me a story"):
        assert getattr(chunk, "scope3ai") is not None
        assert chunk.scope3ai.request.request_duration_ms > 0
        assert chunk.scope3ai.request.input_tokens > 0
        assert chunk.scope3ai.impact is not None
        assert chunk.scope3ai.impact.total_impact is not None
        assert chunk.scope3ai.impact.total_impact.usage_energy_wh > 0
        assert chunk.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
        assert chunk.scope3ai.impact.total_impact.usage_water_ml > 0
        assert chunk.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
        assert chunk.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_gemini_chat_stream_async(tracer_with_sync_init):
    client = Client(api_key=os.environ["GOOGLE_API_KEY"])
    chat = client.aio.chats.create(model="gemini-2.0-flash-exp")
    async for chunk in chat.send_message_stream("tell me a story"):
        assert getattr(chunk, "scope3ai") is not None
        assert chunk.scope3ai.request.request_duration_ms > 0
        assert chunk.scope3ai.request.input_tokens > 0
        assert chunk.scope3ai.impact is not None
        assert chunk.scope3ai.impact.total_impact is not None
        assert chunk.scope3ai.impact.total_impact.usage_energy_wh > 0
        assert chunk.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
        assert chunk.scope3ai.impact.total_impact.usage_water_ml > 0
        assert chunk.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
        assert chunk.scope3ai.impact.total_impact.embodied_water_ml > 0
