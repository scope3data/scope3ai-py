import pytest


# XXX flac is buggy, returning 0.0 duration
# XXX pcm is not supported by mutagen
@pytest.mark.vcr
@pytest.mark.parametrize("audio_format", ["mp3", "opus", "aac", "wav"])  # pcm, flac
@pytest.mark.parametrize("model", ["tts-1", "tts-1-hd"])
def test_openai_tts_wrapper(tracer_with_sync_init, audio_format, model):
    from openai import OpenAI

    client = OpenAI()
    response = client.audio.speech.create(
        model=model,
        voice="alloy",
        input="Hello World!",
        response_format=audio_format,
    )

    assert response is not None
    assert response.scope3ai is not None
    assert response.scope3ai.request.output_audio_seconds is not None
    assert response.scope3ai.request.output_audio_seconds > 0.5
    assert response.scope3ai.request.output_audio_seconds < 3
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("audio_format", ["mp3", "opus", "aac", "wav"])  # pcm, flac
@pytest.mark.parametrize("model", ["tts-1", "tts-1-hd"])
async def test_openai_tts_wrapper_async(tracer_with_sync_init, audio_format, model):
    from openai import AsyncOpenAI

    client = AsyncOpenAI()
    response = await client.audio.speech.create(
        model=model,
        voice="alloy",
        input="Hello World!",
        response_format=audio_format,
    )

    assert response is not None
    assert response.scope3ai is not None
    assert response.scope3ai.request.output_audio_seconds is not None
    assert response.scope3ai.request.output_audio_seconds > 0.5
    assert response.scope3ai.request.output_audio_seconds < 3
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0
