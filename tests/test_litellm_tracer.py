from pathlib import Path

import litellm
import pytest


USE_ALWAYS_LITELLM_TRACER = True


#
@pytest.mark.vcr
def test_litellm_chat(tracer_with_sync_init):
    response = litellm.completion(
        model="huggingface/meta-llama/Meta-Llama-3-8B-Instruct",
        messages=[{"role": "user", "content": "Hello World!"}],
        use_always_litellm_tracer=USE_ALWAYS_LITELLM_TRACER,
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 44
    assert response.scope3ai.request.output_tokens == 69
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_litellm_async_chat(tracer_with_sync_init):
    response = await litellm.acompletion(
        messages=[{"role": "user", "content": "Hello World!"}],
        model="command-r",
        use_always_litellm_tracer=USE_ALWAYS_LITELLM_TRACER,
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 3
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_litellm_stream_chat(tracer_with_sync_init):
    stream = litellm.completion(
        messages=[{"role": "user", "content": "Hello World!"}],
        model="claude-3-5-sonnet-20240620",
        stream=True,
        use_always_litellm_tracer=USE_ALWAYS_LITELLM_TRACER,
    )
    for chunk in stream:
        assert getattr(chunk, "scope3ai") is not None
        assert chunk.scope3ai.impact is not None
        assert chunk.scope3ai.impact.total_impact is not None
        assert chunk.scope3ai.impact.total_impact.usage_energy_wh > 0
        assert chunk.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
        assert chunk.scope3ai.impact.total_impact.usage_water_ml > 0
        assert chunk.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
        assert chunk.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_litellm_async_stream_chat(tracer_with_sync_init):
    stream = await litellm.acompletion(
        messages=[{"role": "user", "content": "Hello World!"}],
        model="claude-3-5-sonnet-20240620",
        stream=True,
        use_always_litellm_tracer=USE_ALWAYS_LITELLM_TRACER,
    )
    async for chunk in stream:
        assert getattr(chunk, "scope3ai") is not None
        assert chunk.scope3ai.impact is not None
        assert chunk.scope3ai.impact.total_impact is not None
        assert chunk.scope3ai.impact.total_impact.usage_energy_wh > 0
        assert chunk.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
        assert chunk.scope3ai.impact.total_impact.usage_water_ml > 0
        assert chunk.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
        assert chunk.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_litellm_image_generation(tracer_with_sync_init):
    response = litellm.image_generation(
        prompt="A serene landscape with mountains and a lake",
        model="dall-e-3",
        use_always_litellm_tracer=USE_ALWAYS_LITELLM_TRACER,
    )
    assert response
    assert len(response.data) > 0
    assert getattr(response, "scope3ai") is not None
    # TODO: Add this assert when AiApi support it
    # assert response.scope3ai.request.managed_service_id == PROVIDERS.LITELLM.value
    assert response.scope3ai.request is not None
    assert response.scope3ai.request.input_tokens == 8
    assert response.scope3ai.request.request_duration_ms > 0
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_litellm_async_image_generation(tracer_with_sync_init):
    response = await litellm.aimage_generation(
        prompt="A futuristic cityscape at night",
        model="dall-e-3",
        use_always_litellm_tracer=USE_ALWAYS_LITELLM_TRACER,
    )
    assert response
    assert len(response.data) > 0
    assert getattr(response, "scope3ai") is not None
    # TODO: Add this assert when AiApi support it
    # assert response.scope3ai.request.managed_service_id == PROVIDERS.LITELLM.value
    assert response.scope3ai.request is not None
    assert response.scope3ai.request.input_tokens == 6
    assert response.scope3ai.request.request_duration_ms > 0
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_litellm_speech_to_text(tracer_with_sync_init):
    datadir = Path(__file__).parent / "data"
    hello_there_audio = open((datadir / "hello_there.mp3").as_posix(), "rb")

    response = litellm.transcription(
        model="whisper-1",
        file=hello_there_audio,
        use_always_litellm_tracer=USE_ALWAYS_LITELLM_TRACER,
    )
    assert response

    assert response.text is not None
    assert len(response.text) > 0
    assert getattr(response, "scope3ai") is not None
    # TODO: Add this assert when AiApi support it
    # assert response.scope3ai.request.managed_service_id == PROVIDERS.LITELLM.value
    assert response.scope3ai.request is not None
    assert response.scope3ai.request.output_tokens == 2
    assert response.scope3ai.request.request_duration_ms > 0
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_litellm_async_speech_to_text(tracer_with_sync_init):
    datadir = Path(__file__).parent / "data"
    hello_there_audio = open((datadir / "hello_there.mp3").as_posix(), "rb")
    response = await litellm.atranscription(
        model="whisper-1",
        file=hello_there_audio,
        use_always_litellm_tracer=USE_ALWAYS_LITELLM_TRACER,
    )
    assert response
    assert response.text is not None
    assert len(response.text) > 0
    assert getattr(response, "scope3ai") is not None
    # TODO: Add this assert when AiApi support it
    # assert response.scope3ai.request.managed_service_id == PROVIDERS.LITELLM.value
    assert response.scope3ai.request is not None
    assert response.scope3ai.request.output_tokens == 2
    assert response.scope3ai.request.request_duration_ms > 0
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_litellm_text_to_speech(tracer_with_sync_init):
    response = litellm.speech(
        model="tts-1",
        input="Hello, this is a test of the speech synthesis system.",
        voice="alloy",
        use_always_litellm_tracer=USE_ALWAYS_LITELLM_TRACER,
    )
    assert response
    assert response.text is not None
    assert len(response.text) > 0
    assert getattr(response, "scope3ai") is not None
    # TODO: Add this assert when AiApi support it
    # assert response.scope3ai.request.managed_service_id == PROVIDERS.LITELLM.value
    assert response.scope3ai.request is not None
    assert response.scope3ai.request.input_tokens == 12
    assert response.scope3ai.request.request_duration_ms > 0
    assert response.scope3ai.request.output_audio_seconds == pytest.approx(3, 0.1)
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_litellm_async_text_to_speech(tracer_with_sync_init):
    response = await litellm.aspeech(
        model="tts-1",
        input="Hello, this is a test of the speech synthesis system.",
        voice="alloy",
        use_always_litellm_tracer=USE_ALWAYS_LITELLM_TRACER,
    )
    assert response
    assert response.text is not None
    assert len(response.text) > 0
    assert getattr(response, "scope3ai") is not None
    # TODO: Add this assert when AiApi support it
    # assert response.scope3ai.request.managed_service_id == PROVIDERS.LITELLM.value
    assert response.scope3ai.request is not None
    assert response.scope3ai.request.input_tokens == 12
    assert response.scope3ai.request.request_duration_ms > 0
    assert response.scope3ai.request.output_audio_seconds == pytest.approx(3, 0.1)
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0
