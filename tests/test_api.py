import pytest


def test_api_get_node(api_client):
    response = api_client.get_node()
    assert response is not None
    assert len(response.nodes)


@pytest.mark.asyncio
async def test_async_api_get_node(async_api_client):
    response = await async_api_client.get_node()
    assert response is not None
    assert len(response.nodes)


def test_api_get_gpu(api_client):
    response = api_client.get_gpu()
    assert response is not None
    assert len(response.gpus)


@pytest.mark.asyncio
async def test_async_api_get_gpu(async_api_client):
    response = await async_api_client.get_gpu()
    assert response is not None
    assert len(response.gpus)


def test_api_get_model(api_client):
    response = api_client.get_model()
    assert response is not None
    assert len(response.models)


@pytest.mark.asyncio
async def test_async_api_get_model(async_api_client):
    response = await async_api_client.get_model()
    assert response is not None
    assert len(response.models)
