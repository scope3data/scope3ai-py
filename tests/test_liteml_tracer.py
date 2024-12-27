import litellm
import pytest


@pytest.mark.vcr
def test_litellm_chat(tracer_init):
    response = litellm.completion(
        model="huggingface/meta-llama/Meta-Llama-3-8B-Instruct",
        messages=[{"role": "user", "content": "Hello World!"}],
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.request_id is not None
    assert response.scope3ai.request.input_tokens == 44
    assert response.scope3ai.request.output_tokens == 69
    assert response.scope3ai.impact is None
