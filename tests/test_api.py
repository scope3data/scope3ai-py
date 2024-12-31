import pytest


def test_api_node(api_client):
    response = api_client.node()
    assert response is not None
    assert len(response.nodes)


@pytest.mark.asyncio
async def test_async_api_node(async_api_client):
    response = await async_api_client.node()
    assert response is not None
    assert len(response.nodes)


def test_api_gpu(api_client):
    response = api_client.gpu()
    assert response is not None
    assert len(response.gpus)


@pytest.mark.asyncio
async def test_async_api_gpu(async_api_client):
    response = await async_api_client.gpu()
    assert response is not None
    assert len(response.gpus)


def test_api_model(api_client):
    response = api_client.model()
    assert response is not None
    assert len(response.models)


@pytest.mark.asyncio
async def test_async_api_model(async_api_client):
    response = await async_api_client.model()
    assert response is not None
    assert len(response.models)
