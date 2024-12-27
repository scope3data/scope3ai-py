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
    assert response.scope3ai.request.input_tokens == 44
    assert response.scope3ai.request.output_tokens == 69
    assert response.scope3ai.impact is None


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_litellm_async_chat(tracer_init):
    response = await litellm.acompletion(
        messages=[{"role": "user", "content": "Hello World!"}],
        model="huggingface/meta-llama/Meta-Llama-3-8B-Instruct",
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 44
    assert response.scope3ai.impact is None


@pytest.mark.vcr
def test_litellm_stream_chat(tracer_init):
    stream = litellm.completion(
        messages=[{"role": "user", "content": "Hello World!"}],
        model="huggingface/meta-llama/Meta-Llama-3-8B-Instruct",
        stream=True,
    )
    for chunk in stream:
        assert getattr(chunk, "scope3ai") is not None
        assert chunk.scope3ai.impact is None


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_litellm_async_stream_chat(tracer_init):
    stream = await litellm.acompletion(
        messages=[{"role": "user", "content": "Hello World!"}],
        model="huggingface/meta-llama/Meta-Llama-3-8B-Instruct",
        stream=True,
    )
    async for chunk in stream:
        assert getattr(chunk, "scope3ai") is not None
        assert chunk.scope3ai.impact is None
