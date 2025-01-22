import pytest
import litellm

from scope3ai.api.typesgen import Image
from scope3ai.constants import PROVIDERS
from tests.utils import (
    load_image_b64,
    TEST_IMAGE_PNG,
    file_as_b64str,
    TEST_AUDIO_MP3,
    TEST_IMAGE_JPG,
    TEST_AUDIO_WAV,
)

USE_ALWAYS_LITELLM_TRACER = False


@pytest.mark.vcr
def test_litellm_multimodal_vision_openai(tracer_with_sync_init):
    response = litellm.completion(
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
        use_always_litellm_tracer=USE_ALWAYS_LITELLM_TRACER,
        api_version="2024-02-15-preview",
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.managed_service_id == PROVIDERS.OPENAI.value
    assert response.scope3ai.request.input_tokens == 872
    assert response.scope3ai.request.output_tokens == 59
    assert response.scope3ai.request.input_images == [Image(root="1024x1024")]
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_litellm_multimodal_vision_2_images_openai(tracer_with_sync_init):
    from scope3ai.api.typesgen import Image

    response = litellm.completion(
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
        use_always_litellm_tracer=USE_ALWAYS_LITELLM_TRACER,
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.managed_service_id == PROVIDERS.OPENAI.value
    assert response.scope3ai.request.input_tokens == 1082
    assert response.scope3ai.request.output_tokens == 54
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
def test_litellm_multimodal_audio_openai(tracer_with_sync_init):
    response = litellm.completion(
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
        use_always_litellm_tracer=USE_ALWAYS_LITELLM_TRACER,
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.managed_service_id == PROVIDERS.OPENAI.value
    assert response.scope3ai.request.input_tokens == 29
    assert response.scope3ai.request.output_tokens == 10
    assert response.scope3ai.request.input_audio_seconds >= 1
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_litellm_multimodal_audio_2_openai(tracer_with_sync_init):
    response = litellm.completion(
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
        use_always_litellm_tracer=USE_ALWAYS_LITELLM_TRACER,
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.managed_service_id == PROVIDERS.OPENAI.value
    assert response.scope3ai.request.input_tokens == 46
    assert response.scope3ai.request.output_tokens == 35
    assert response.scope3ai.request.input_audio_seconds >= 1
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_litellm_multimodal_vision_mistralai(tracer_with_sync_init):
    response = litellm.completion(
        model="mistral/pixtral-12b-2409",
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
        api_version="2024-02-15-preview",
        use_always_litellm_tracer=USE_ALWAYS_LITELLM_TRACER,
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.managed_service_id == PROVIDERS.OPENAI.value
    assert response.scope3ai.request.input_tokens == 4172
    assert response.scope3ai.request.output_tokens == 81
    assert response.scope3ai.request.input_images == [Image(root="1024x1024")]
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_litellm_multimodal_vision_2_images_mistralai(tracer_with_sync_init):
    from scope3ai.api.typesgen import Image

    response = litellm.completion(
        model="mistral/pixtral-12b-2409",
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
        use_always_litellm_tracer=USE_ALWAYS_LITELLM_TRACER,
    )
    assert len(response.choices) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.managed_service_id == PROVIDERS.OPENAI.value
    assert response.scope3ai.request.input_tokens == 5228
    assert response.scope3ai.request.output_tokens == 109
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
