from pathlib import Path

import pytest
from huggingface_hub import InferenceClient, AsyncInferenceClient

from scope3ai.api.typesgen import Image


@pytest.mark.vcr
def test_huggingface_hub_chat(tracer_with_sync_init):
    client = InferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct")
    response = client.chat_completion(
        messages=[{"role": "user", "content": "Hello World!"}], max_tokens=15
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 13
    assert response.scope3ai.request.output_tokens == 4
    assert response.scope3ai.request.request_duration_ms == pytest.approx(87.5, 0.1)
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_huggingface_hub_async_chat(tracer_with_sync_init):
    client = AsyncInferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct")
    response = await client.chat_completion(
        messages=[{"role": "user", "content": "Hello World!"}], max_tokens=15
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None


@pytest.mark.vcr
def test_huggingface_hub_stream_chat(tracer_with_sync_init):
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
async def test_huggingface_hub_async_stream_chat(tracer_with_sync_init):
    client = AsyncInferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct")
    async for token in await client.chat_completion(
        [{"role": "user", "content": "Hello World!"}], max_tokens=10, stream=True
    ):
        assert getattr(token, "scope3ai") is not None


@pytest.mark.vcr
def test_huggingface_hub_image_generation(tracer_with_sync_init):
    client = InferenceClient()
    response = client.text_to_image(prompt="An astronaut riding a horse on the moon.")
    assert response.image
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 9
    assert len(response.scope3ai.request.output_images) == 1
    assert response.scope3ai.request.request_duration_ms == pytest.approx(18850, 0.1)
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_huggingface_hub_image_generation_async(tracer_with_sync_init):
    client = AsyncInferenceClient()
    response = await client.text_to_image("An astronaut riding a horse on the moon.")
    assert response.image
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 9
    assert len(response.scope3ai.request.output_images) == 1
    assert response.scope3ai.request.request_duration_ms == pytest.approx(18850, 0.1)
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_huggingface_hub_translation(tracer_with_sync_init):
    client = InferenceClient()
    response = client.translation(
        "My name is Wolfgang and I live in Berlin", model="Helsinki-NLP/opus-mt-en-fr"
    )
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_huggingface_hub_translation_async(tracer_with_sync_init):
    client = AsyncInferenceClient()
    response = await client.translation(
        "My name is Wolfgang and I live in Berlin", model="Helsinki-NLP/opus-mt-en-fr"
    )
    assert response.scope3ai.request.request_duration_ms == 262
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_huggingface_hub_speech_to_text(tracer_with_sync_init):
    datadir = Path(__file__).parent / "data"
    client = InferenceClient()
    response = client.automatic_speech_recognition(
        audio=(datadir / "hello_there.mp3").as_posix()
    )
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.request_duration_ms == 385.0
    assert response.scope3ai.request.input_audio_seconds == 0
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_huggingface_hub_speech_to_text_async(tracer_with_sync_init):
    client = AsyncInferenceClient()
    datadir = Path(__file__).parent / "data"
    hello_there_audio = open((datadir / "hello_there.mp3").as_posix(), "rb")
    hello_there_audio_bytes = hello_there_audio.read()
    response = await client.automatic_speech_recognition(
        audio=hello_there_audio_bytes,
    )
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.request_duration_ms == 385.0
    assert response.scope3ai.request.input_audio_seconds == 0
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_huggingface_hub_text_to_speech(tracer_with_sync_init):
    client = InferenceClient()
    response = client.text_to_speech("Hello World!")
    assert response.scope3ai.request.request_duration_ms == 5332
    assert response.scope3ai.request.input_tokens == 12
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_huggingface_hub_text_to_speech_async(tracer_with_sync_init):
    client = AsyncInferenceClient()
    response = await client.text_to_speech("Hello World!")
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.request_duration_ms == 5332
    assert response.scope3ai.request.input_tokens == 3
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_huggingface_hub_image_to_image(tracer_with_sync_init):
    client = InferenceClient()
    datadir = Path(__file__).parent / "data"
    response = client.image_to_image(
        (datadir / "cat.png").as_posix(),
        "cat wizard, gandalf, lord of the rings, detailed, fantasy, cute, adorable, Pixar, Disney, 8k",
        model="stabilityai/stable-diffusion-xl-refiner-1.0",
    )
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.request_duration_ms == 2543
    assert response.scope3ai.request.output_images == [Image(root="1024x704")]
    assert response.scope3ai.request.input_images == [Image(root="1024x704")]
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_huggingface_hub_image_to_image_async(tracer_with_sync_init):
    client = AsyncInferenceClient()
    datadir = Path(__file__).parent / "data"
    response = await client.image_to_image(
        (datadir / "image_1024.png").as_posix(),
        "Cat dancing in the moon",
        model="stabilityai/stable-diffusion-xl-refiner-1.0",
    )
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.request_duration_ms == 6467
    assert response.scope3ai.request.output_images == [Image(root="1024x1024")]
    assert response.scope3ai.request.input_images == [Image(root="1024x1024")]
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.parametrize(
    "image_type",
    ["str", "Path", "bytes"],
)
@pytest.mark.asyncio
async def test_huggingface_hub_object_detection_async(
    tracer_with_sync_init, image_type
):
    client = AsyncInferenceClient()
    datadir = Path(__file__).parent / "data"

    path = datadir / "street_scene.png"
    if image_type == "str":
        street_scene_image = path.as_posix()
    elif image_type == "Path":
        street_scene_image = path
    elif image_type == "bytes":
        street_scene_image = path.read_bytes()
    else:
        assert 0
        return

    response = await client.object_detection(street_scene_image)
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_images == [Image(root="1024x1024")]
    assert response.scope3ai.request.request_duration_ms > 0
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_huggingface_hub_object_detection(tracer_with_sync_init):
    client = InferenceClient()
    datadir = Path(__file__).parent / "data"
    response = client.object_detection((datadir / "street_scene.png").as_posix())
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_images == [Image(root="1024x1024")]
    assert response.scope3ai.request.request_duration_ms == 657
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_huggingface_hub_image_segmentation_async(tracer_with_sync_init):
    client = AsyncInferenceClient()
    datadir = Path(__file__).parent / "data"
    dog_image = open((datadir / "dog.png").as_posix(), "rb")
    dog_image_bytes = dog_image.read()
    response = await client.image_segmentation(dog_image_bytes)
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_images == [Image(root="1024x1024")]
    assert response.scope3ai.request.request_duration_ms == 686
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_huggingface_hub_image_segmentation(tracer_with_sync_init):
    client = InferenceClient()
    datadir = Path(__file__).parent / "data"
    response = client.image_segmentation((datadir / "dog.png").as_posix())
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_images == [Image(root="1024x1024")]
    assert response.scope3ai.request.request_duration_ms == 686
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_huggingface_hub_image_classification_async(tracer_with_sync_init):
    client = AsyncInferenceClient()
    datadir = Path(__file__).parent / "data"
    cat_image = open((datadir / "cat.png").as_posix(), "rb")
    cat_image_bytes = cat_image.read()
    response = await client.image_classification(cat_image_bytes)
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_images == [Image(root="1024x704")]
    assert response.scope3ai.request.request_duration_ms == 226
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_huggingface_hub_image_classification(tracer_with_sync_init):
    client = InferenceClient()
    datadir = Path(__file__).parent / "data"
    response = client.image_classification((datadir / "cat.png").as_posix())
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_images == [Image(root="1024x704")]
    assert response.scope3ai.request.request_duration_ms == 226
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0
