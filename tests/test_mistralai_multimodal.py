import pytest
from mistralai import Mistral

from scope3ai.api.typesgen import Image
from tests.utils import load_image_b64, TEST_IMAGE_PNG, TEST_IMAGE_JPG


@pytest.mark.vcr
def test_mistralai_multimodal_vision(tracer_with_sync_init):
    client = Mistral()
    response = client.chat.complete(
        model="pixtral-12b-2409",
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
    assert response.scope3ai.request.input_tokens == 4172
    assert response.scope3ai.request.output_tokens == 105
    assert response.scope3ai.request.input_images == [Image(root="1024x1024")]
    assert response.scope3ai.impact is not None
    assert response.scope3ai.impact.total_impact is not None
    assert response.scope3ai.impact.total_impact.usage_energy_wh > 0
    assert response.scope3ai.impact.total_impact.usage_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.usage_water_ml > 0
    assert response.scope3ai.impact.total_impact.embodied_emissions_gco2e > 0
    assert response.scope3ai.impact.total_impact.embodied_water_ml > 0


@pytest.mark.vcr
def test_mistralai_multimodal_vision_2_images(tracer_with_sync_init):
    client = Mistral()
    response = client.chat.complete(
        model="pixtral-12b-2409",
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
    assert response.scope3ai.request.input_tokens == 5228
    assert response.scope3ai.request.output_tokens == 108
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
