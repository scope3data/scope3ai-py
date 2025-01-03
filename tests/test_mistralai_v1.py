import pytest
from mistralai import Mistral


@pytest.mark.vcr
def test_mistralai_chat(tracer_init):
    client = Mistral()
    response = client.chat.complete(
        messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 6
    assert response.scope3ai.request.output_tokens == 18
    assert response.scope3ai.impact is None


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_mistralai_async_chat(tracer_init):
    client = Mistral()
    response = await client.chat.complete_async(
        messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 6
    assert response.scope3ai.request.output_tokens == 18
    assert response.scope3ai.impact is None


@pytest.mark.vcr
def test_mistralai_stream_chat(tracer_init):
    client = Mistral()
    stream = client.chat.stream(
        messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
    )
    for chunk in stream:
        assert getattr(chunk.data, "scope3ai") is not None


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_mistralai_async_stream_chat(tracer_init):
    client = Mistral()
    stream = await client.chat.stream_async(
        messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
    )
    async for chunk in stream:
        assert getattr(chunk.data, "scope3ai") is not None
