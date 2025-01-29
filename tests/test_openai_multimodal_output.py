import pytest

from scope3ai.constants import PROVIDERS


@pytest.mark.vcr
def test_openai_multimodal_output(tracer_with_sync_init):
    from openai import OpenAI

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
        messages=[
            {"role": "user", "content": "Is a golden retriever a good family dog?"}
        ],
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.managed_service_id == PROVIDERS.OPENAI.value
    assert response.scope3ai.request.input_tokens == 17
    assert response.scope3ai.request.output_tokens == 415
    assert response.scope3ai.request.output_audio_seconds > 0
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0
