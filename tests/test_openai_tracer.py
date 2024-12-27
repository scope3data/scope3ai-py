import pytest
from openai import OpenAI


@pytest.mark.vcr
def test_openai_chat(tracer_init):
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
def test_openai_chat_with_response(tracer_with_response_init):
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
