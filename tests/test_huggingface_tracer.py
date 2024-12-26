import pytest
from pathlib import Path
from huggingface_hub import InferenceClient


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
def test_huggingface_hub_translation(tracer_init):
    client = InferenceClient()
    client.translation(
        "My name is Wolfgang and I live in Berlin", model="Helsinki-NLP/opus-mt-en-fr"
    )


# @pytest.mark.vcr
# def test_huggingface_hub_text_to_speech(tracer_init):
#     client = InferenceClient(token="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")
#     client.text_to_speech(
#         "Even use the service to create audiobooks", model="suno/bark-small"
#     )


@pytest.mark.vcr
def test_huggingface_hub_speech_to_text(tracer_init):
    datadir = Path(__file__).parent / "data"
    client = InferenceClient()
    response = client.automatic_speech_recognition(
        audio=(datadir / "hello_there.mp3").as_posix()
    )
    assert getattr(response, "scope3ai") is not None
