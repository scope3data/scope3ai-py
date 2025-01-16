import base64
from pathlib import Path

import pytest

TEST_IMAGE_PNG = Path(__file__).parent / "data" / "image_1024.png"
TEST_IMAGE_JPG = Path(__file__).parent / "data" / "image_512.jpg"
TEST_AUDIO_MP3 = Path(__file__).parent / "data" / "hello_there.mp3"
TEST_AUDIO_WAV = Path(__file__).parent / "data" / "hello_there.wav"


def file_as_b64str(path: Path) -> str:
    data = path.read_bytes()
    return base64.b64encode(data).decode("utf-8")


def load_image_b64(path: Path) -> str:
    media_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }
    b64 = file_as_b64str(path)
    media_type = media_types[path.suffix]
    return f"data:{media_type};base64,{b64}"


@pytest.mark.vcr
def test_openai_multimodal_vision(tracer_with_sync_init):
    from openai import OpenAI

    from scope3ai.api.typesgen import Image

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Hello World! What's the image about ?",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": load_image_b64(TEST_IMAGE_PNG),
                        },
                    },
                ],
            },
        ],
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 872
    assert response.scope3ai.request.output_tokens == 57
    assert response.scope3ai.request.input_images == [Image(root="1024x1024")]
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_openai_multimodal_vision_2_images(tracer_with_sync_init):
    from openai import OpenAI

    from scope3ai.api.typesgen import Image

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Hello World! What's the image about ?",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": load_image_b64(TEST_IMAGE_JPG),
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": load_image_b64(TEST_IMAGE_PNG),
                        },
                    },
                ],
            },
        ],
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 34016
    assert response.scope3ai.request.output_tokens == 47
    assert response.scope3ai.request.input_images == [
        Image(root="512x512"),
        Image(root="1024x1024"),
    ]
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_openai_multimodal_audio(tracer_with_sync_init):
    from openai import OpenAI

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's the audio about ?",
                    },
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": file_as_b64str(TEST_AUDIO_MP3),
                            "format": "mp3",
                        },
                    },
                ],
            },
        ],
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 29
    assert response.scope3ai.request.output_tokens == 15
    assert response.scope3ai.request.input_audio_seconds >= 1
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_openai_multimodal_audio_2(tracer_with_sync_init):
    from openai import OpenAI

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-audio-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's the audio about ?",
                    },
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": file_as_b64str(TEST_AUDIO_MP3),
                            "format": "mp3",
                        },
                    },
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": file_as_b64str(TEST_AUDIO_WAV),
                            "format": "wav",
                        },
                    },
                ],
            },
        ],
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 46
    assert response.scope3ai.request.output_tokens == 17
    assert response.scope3ai.request.input_audio_seconds >= 1
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


# XXX openai does not support audio and image yet.
# the model audio-preview does not support image_url
# and the model gpt-4o does not support input_audio
# not even o1 support audio and image and text.
# @pytest.mark.vcr
# def test_openai_multimodal_audio_and_image(tracer_with_sync_init):
#     from openai import OpenAI
#
#     client = OpenAI()
#     response = client.chat.completions.create(
#         model="gpt-4o-audio-preview",
#         messages=[
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": "Identify the image and what it says.",
#                     },
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": load_image_b64(TEST_IMAGE_JPG),
#                         },
#                     },
#                     {
#                         "type": "input_audio",
#                         "input_audio": {
#                             "data": file_as_b64str(TEST_AUDIO_MP3),
#                             "format": "mp3",
#                         },
#                     },
#                 ],
#             },
#         ],
#     )
#     assert len(response.choices) > 0
#     assert getattr(response, "scope3ai") is not None
#     assert response.scope3ai.request.input_tokens == 29
#     assert response.scope3ai.request.output_tokens == 15
#     assert response.scope3ai.request.input_images == "512x512"
#     assert response.scope3ai.request.input_audio_seconds > 0
#     assert response.scope3ai.impact is not None
#     assert response.scope3ai.impact.total_impact is not None
#     assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
#     assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
#     assert response.scope3ai.impact.total_impact.usage_water_ml > 0
#     assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
#     assert response.scope3ai.impact.total_impact.embodied_water_ml > 0
