import pytest
import pathlib

TEST_IMAGE = pathlib.Path(__file__).parent / "data" / "image_1024.png"
TEST_MASK = pathlib.Path(__file__).parent / "data" / "mask_1024.png"


@pytest.mark.vcr
@pytest.mark.parametrize("image_size", ["256x256", "512x512", None])
@pytest.mark.parametrize("n", [1, 2])
@pytest.mark.parametrize("model", ["dall-e-2", None])
def test_openai_image_wrapper(tracer_init, image_size, n, model):
    from openai import OpenAI

    kwargs = {}
    if image_size is not None:
        kwargs["size"] = image_size
    if model is not None:
        kwargs["model"] = model

    client = OpenAI()
    response = client.images.generate(
        prompt="A beautiful landscape",
        n=n,
        **kwargs,
    )

    assert response is not None
    assert response.scope3ai is not None
    assert response.scope3ai.request.output_images is not None
    assert len(response.scope3ai.request.output_images) == n


@pytest.mark.vcr
@pytest.mark.parametrize("n", [1, 2])
@pytest.mark.parametrize("model", ["dall-e-2", None])
def test_openai_image_create_variation_wrapper(tracer_init, n, model):
    from openai import OpenAI

    kwargs = {}
    if model is not None:
        kwargs["model"] = model

    client = OpenAI()
    response = client.images.create_variation(
        image=TEST_IMAGE,
        n=n,
        **kwargs,
    )

    assert response is not None
    assert response.scope3ai is not None
    assert response.scope3ai.request.output_images is not None
    assert len(response.scope3ai.request.output_images) == n


@pytest.mark.vcr
@pytest.mark.parametrize("n", [1, 2])
@pytest.mark.parametrize("model", ["dall-e-2", None])
def test_openai_image_edit_wrapper(tracer_init, n, model):
    from openai import OpenAI

    kwargs = {}
    if model is not None:
        kwargs["model"] = model

    client = OpenAI()
    response = client.images.edit(
        image=TEST_IMAGE,
        mask=TEST_MASK,
        prompt="Add a sunset",
        n=n,
        **kwargs,
    )

    assert response is not None
    assert response.scope3ai is not None
    assert response.scope3ai.request.output_images is not None
    assert len(response.scope3ai.request.output_images) == n


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("n", [1, 2])
@pytest.mark.parametrize("model", ["dall-e-2", None])
async def test_openai_image_generate_wrapper_async(tracer_init, n, model):
    from openai import AsyncOpenAI

    kwargs = {}
    if model is not None:
        kwargs["model"] = model

    client = AsyncOpenAI()
    response = await client.images.generate(
        prompt="A beautiful landscape",
        n=n,
        **kwargs,
    )

    assert response is not None
    assert response.scope3ai is not None
    assert response.scope3ai.request.output_images is not None
    assert len(response.scope3ai.request.output_images) == n


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("n", [1, 2])
@pytest.mark.parametrize("model", ["dall-e-2", None])
async def test_openai_image_create_variation_wrapper_async(tracer_init, n, model):
    from openai import AsyncOpenAI

    kwargs = {}
    if model is not None:
        kwargs["model"] = model

    client = AsyncOpenAI()
    response = await client.images.create_variation(
        image=TEST_IMAGE,
        n=n,
        **kwargs,
    )

    assert response is not None
    assert response.scope3ai is not None
    assert response.scope3ai.request.output_images is not None
    assert len(response.scope3ai.request.output_images) == n


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("n", [1, 2])
@pytest.mark.parametrize("model", ["dall-e-2", None])
async def test_openai_image_edit_wrapper_async(tracer_init, n, model):
    from openai import AsyncOpenAI

    kwargs = {}
    if model is not None:
        kwargs["model"] = model

    client = AsyncOpenAI()
    response = await client.images.edit(
        image=TEST_IMAGE,
        mask=TEST_MASK,
        prompt="Add a sunset",
        n=n,
        **kwargs,
    )

    assert response is not None
    assert response.scope3ai is not None
    assert response.scope3ai.request.output_images is not None
    assert len(response.scope3ai.request.output_images) == n
