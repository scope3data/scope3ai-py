import litellm
import pytest


@pytest.mark.vcr
@pytest.mark.parametrize("audio_format", ["wav", "mp3", "flac", "opus"])
def test_litellm_multimodal_output_openai(tracer_with_sync_init, audio_format):
    response = litellm.completion(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": audio_format},
        messages=[
            {"role": "user", "content": "Is a golden retriever a good family dog?"}
        ],
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    # TODO: Add this assert when AiApi support it
    # assert response.scope3ai.request.managed_service_id == PROVIDERS.OPENAI.value

    assert response.scope3ai.request.input_tokens == 17
    assert response.scope3ai.request.output_tokens > 0
    assert response.scope3ai.request.output_audio_seconds > 0
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.parametrize("audio_format", ["wav", "mp3", "flac", "opus"])
def test_litellm_multimodal_output_default(tracer_with_sync_init, audio_format):
    response = litellm.completion(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": audio_format},
        messages=[
            {"role": "user", "content": "Is a golden retriever a good family dog?"}
        ],
        use_always_litellm_tracer=True,
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    # TODO: Add this assert when AiApi support it
    # assert response.scope3ai.request.managed_service_id == PROVIDERS.LITELLM.value
    assert response.scope3ai.request.input_tokens == 17
    assert response.scope3ai.request.output_tokens > 0
    assert response.scope3ai.request.output_audio_seconds > 0
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("audio_format", ["wav", "mp3", "flac", "opus"])
async def test_litellm_multimodal_output_openai_async(
    tracer_with_sync_init, audio_format
):
    response = await litellm.acompletion(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": audio_format},
        messages=[
            {"role": "user", "content": "Is a golden retriever a good family dog?"}
        ],
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    # TODO: Add this assert when AiApi support it
    # assert response.scope3ai.request.managed_service_id == PROVIDERS.OPENAI.value

    assert response.scope3ai.request.input_tokens == 17
    assert response.scope3ai.request.output_tokens > 0
    assert response.scope3ai.request.output_audio_seconds > 0
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("audio_format", ["wav", "mp3", "flac", "opus"])
async def test_litellm_multimodal_output_default_async(
    tracer_with_sync_init, audio_format
):
    response = await litellm.acompletion(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": audio_format},
        messages=[
            {"role": "user", "content": "Is a golden retriever a good family dog?"}
        ],
        use_always_litellm_tracer=True,
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    # TODO: Add this assert when AiApi support it
    # assert response.scope3ai.request.managed_service_id == PROVIDERS.LITELLM.value
    assert response.scope3ai.request.input_tokens == 17
    assert response.scope3ai.request.output_tokens > 0
    assert response.scope3ai.request.output_audio_seconds > 0
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0
