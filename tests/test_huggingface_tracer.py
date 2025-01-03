from pathlib import Path

import pytest
from huggingface_hub import InferenceClient, AsyncInferenceClient


@pytest.mark.vcr
def test_huggingface_hub_chat(tracer_init):
    client = InferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct")
    response = client.chat_completion(
        messages=[{"role": "user", "content": "Hello World!"}], max_tokens=15
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 13
    assert response.scope3ai.request.output_tokens == 4
    assert response.scope3ai.impact is None
    assert response.scope3ai.request.request_duration_ms == pytest.approx(87.5, 0.1)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_huggingface_hub_async_chat(tracer_init):
    client = AsyncInferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct")
    response = await client.chat_completion(
        messages=[{"role": "user", "content": "Hello World!"}], max_tokens=15
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None


@pytest.mark.vcr
def test_huggingface_hub_stream_chat(tracer_init):
    client = InferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct")
    stream = client.chat_completion(
        messages=[{"role": "user", "content": "Hello World!"}],
        max_tokens=15,
        stream=True,
    )
    for chunk in stream:
        assert getattr(chunk, "scope3ai") is not None


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_huggingface_hub_async_stream_chat(tracer_init):
    client = AsyncInferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct")
    async for token in await client.chat_completion(
        [{"role": "user", "content": "Hello World!"}], max_tokens=10, stream=True
    ):
        assert getattr(token, "scope3ai") is not None


@pytest.mark.vcr
def test_huggingface_hub_image_generation(tracer_init):
    client = InferenceClient()
    response = client.text_to_image(prompt="An astronaut riding a horse on the moon.")
    assert response.image
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 9
    assert len(response.scope3ai.request.output_images) == 1
    assert response.scope3ai.impact is None
    assert response.scope3ai.request.request_duration_ms == pytest.approx(18850, 0.1)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_huggingface_hub_image_generation_async(tracer_init):
    client = AsyncInferenceClient()
    image = await client.text_to_image("An astronaut riding a horse on the moon.")
    assert image


@pytest.mark.vcr
def test_huggingface_hub_translation(tracer_init):
    client = InferenceClient()
    client.translation(
        "My name is Wolfgang and I live in Berlin", model="Helsinki-NLP/opus-mt-en-fr"
    )


@pytest.mark.vcr
def test_huggingface_hub_speech_to_text(tracer_init):
    datadir = Path(__file__).parent / "data"
    client = InferenceClient()
    response = client.automatic_speech_recognition(
        audio=(datadir / "hello_there.mp3").as_posix()
    )
    assert getattr(response, "scope3ai") is not None
