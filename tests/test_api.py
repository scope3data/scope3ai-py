import pytest


def test_api_list_nodes(api_client):
    response = api_client.list_nodes()
    assert response is not None
    assert len(response.nodes)


@pytest.mark.asyncio
async def test_async_api_list_nodes(async_api_client):
    response = await async_api_client.list_nodes()
    assert response is not None
    assert len(response.nodes)


def test_api_get_node(api_client):
    # First get a list of nodes to get a valid ID
    list_response = api_client.list_nodes()
    assert list_response.nodes
    node_id = list_response.nodes[0].id
    
    # Now test get_node with a specific ID
    response = api_client.get_node(node_id)
    assert response is not None


@pytest.mark.asyncio
async def test_async_api_get_node(async_api_client):
    # First get a list of nodes to get a valid ID
    list_response = await async_api_client.list_nodes()
    assert list_response.nodes
    node_id = list_response.nodes[0].id
    
    # Now test get_node with a specific ID
    response = await async_api_client.get_node(node_id)
    assert response is not None


def test_api_list_gpus(api_client):
    response = api_client.list_gpus()
    assert response is not None
    assert len(response.gpus)


@pytest.mark.asyncio
async def test_async_api_list_gpus(async_api_client):
    response = await async_api_client.list_gpus()
    assert response is not None
    assert len(response.gpus)


def test_api_get_gpu(api_client):
    # First get a list of GPUs to get a valid ID
    list_response = api_client.list_gpus()
    assert list_response.gpus
    gpu_id = list_response.gpus[0].id
    
    # Now test get_gpu with a specific ID
    response = api_client.get_gpu(gpu_id)
    assert response is not None


@pytest.mark.asyncio
async def test_async_api_get_gpu(async_api_client):
    # First get a list of GPUs to get a valid ID
    list_response = await async_api_client.list_gpus()
    assert list_response.gpus
    gpu_id = list_response.gpus[0].id
    
    # Now test get_gpu with a specific ID
    response = await async_api_client.get_gpu(gpu_id)
    assert response is not None


def test_api_list_models(api_client):
    response = api_client.list_models()
    assert response is not None
    assert len(response.models)


@pytest.mark.asyncio
async def test_async_api_list_models(async_api_client):
    response = await async_api_client.list_models()
    assert response is not None
    assert len(response.models)


def test_api_get_model(api_client):
    # First get a list of models to get a valid ID
    list_response = api_client.list_models()
    assert list_response.models
    model_id = list_response.models[0].id
    
    # Now test get_model with a specific ID
    response = api_client.get_model(model_id)
    assert response is not None


@pytest.mark.asyncio
async def test_async_api_get_model(async_api_client):
    # First get a list of models to get a valid ID
    list_response = await async_api_client.list_models()
    assert list_response.models
    model_id = list_response.models[0].id
    
    # Now test get_model with a specific ID
    response = await async_api_client.get_model(model_id)
    assert response is not None
