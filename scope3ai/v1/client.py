from os import getenv
from typing import List, Optional, Union

import httpx
from pydantic import BaseModel

from .defaults import DEFAULT_API_URL
from .types import (
    GpuResponse,
    ImpactRequest,
    ImpactRequestRow,
    ImpactResponse,
    ModelFamily,
    ModelResponse,
    NodeCloud,
    NodeResponse,
    NodeService,
)


class Scope3AIError(Exception):
    pass


class ClientBase:
    def __init__(self, api_key: str = None, api_url: str = None) -> None:
        self.api_key = api_key or getenv("SCOPE3AI_API_KEY")
        self.api_url = api_url or getenv("SCOPE3AI_API_URL") or DEFAULT_API_URL
        if not self.api_key:
            raise Scope3AIError(
                "The scope3 api_key option must be set either by "
                "passing the API key to the Scope3AI.init(api_key='xxx') "
                "or by setting the SCOPE3AI_API_KEY environment variable"
            )
        if not self.api_url:
            raise Scope3AIError(
                "The api_url option must be set either by "
                "passing the API URL to the Scope3AI.init(api_url='xxx') "
                "or by setting the SCOPE3AI_API_URL environment variable"
            )

    @property
    def client(self) -> Union[httpx.Client, httpx.AsyncClient]:
        """
        Obtain an httpx client for synchronous or asynchronous operation
        with the necessary authentication headers included.
        """
        if not hasattr(self, "_client"):
            self._client = self.create_client()
        return self._client


class ClientCommands:
    def model(
        self,
        family: Optional[ModelFamily] = None,
    ) -> ModelResponse:
        """
        List models
        """
        params = {}
        if family:
            params["family"] = family
        return self.execute_request(
            "/model",
            method="GET",
            params=params,
            response_model=ModelResponse,
        )

    def gpu(self) -> GpuResponse:
        """
        List GPUs
        """
        return self.execute_request(
            "/gpu",
            method="GET",
            response_model=GpuResponse,
        )

    def node(
        self,
        service: Optional[NodeService] = None,
        cloud: Optional[NodeCloud] = None,
    ) -> NodeResponse:
        """
        List nodes
        """
        params = {}
        if service:
            params["service"] = service.value
        if cloud:
            params["cloud"] = cloud.value
        return self.execute_request(
            "/node",
            method="GET",
            params=params,
            response_model=NodeResponse,
        )

    def impact(
        self,
        rows: List[ImpactRequestRow],
        debug: Optional[bool] = None,
    ) -> ImpactResponse:
        """
        Get impact metrics for a task
        """
        params = {}
        if debug is not None:
            params["debug"] = debug
        json_body = ImpactRequest(rows=rows).model_dump(mode="json")
        return self.execute_request(
            "/v1/impact",
            method="POST",
            params=params,
            json=json_body,
            response_model=ImpactResponse,
        )


class Client(ClientBase, ClientCommands):
    """
    Synchronous Client to the Scope3AI HTTP API
    """

    def create_client(self):
        return httpx.Client(headers={"Authorization": f"Bearer {self.api_key}"})

    def execute_request(
        self,
        url: str,
        method="GET",
        params: Optional[dict] = None,
        json: Optional[dict] = None,
        response_model: Optional[BaseModel] = None,
    ):
        full_url = self.api_url + url
        kwargs = {}
        if params:
            kwargs["params"] = params
        if json:
            kwargs["json"] = json
        response = self.client.request(method, full_url, **kwargs)
        if response_model:
            return response_model.parse_obj(response.json())
        return response.json()


class AsyncClient(ClientBase, ClientCommands):
    """
    Asynchronous Client to the Scope3AI HTTP API
    """

    def create_client(self):
        return httpx.AsyncClient(headers={"Authorization": f"Bearer {self.api_key}"})

    async def execute_request(
        self,
        url: str,
        method="GET",
        params: Optional[dict] = None,
        json: Optional[dict] = None,
        response_model: Optional[BaseModel] = None,
    ):
        full_url = self.api_url + url
        kwargs = {}
        if params:
            kwargs["params"] = params
        if json:
            kwargs["json"] = json
        response = await self.client.request(method, full_url, **kwargs)
        if response_model:
            return response_model.model_validate(response.json())
        return response.json()


if __name__ == "__main__":
    from .types import Model

    funcs_to_test = [
        ["model", {}],
        ["model", {"family": ModelFamily.CLAUDE}],
        ["gpu", {}],
        ["node", {}],
        ["node", {"cloud": NodeCloud.AWS}],
        # ["node", {"service": NodeService.AZURE_ML}],
        ["impact", {"rows": []}],
        [
            "impact",
            {
                "rows": [
                    ImpactRequestRow(
                        model=Model(id="gpt_4o"),
                        input_tokens=1000,
                        output_tokens=200,
                    )
                ]
            },
        ],
    ]

    def test_sync_client():
        print("Testing synchronous client")
        client = Client()
        for name, kwargs in funcs_to_test:
            print(f"- testing {name} with kwargs {kwargs}")
            func = getattr(client, name)
            result = func(**kwargs)
            print(f"{result}")

    async def test_async_client():
        print("Testing asynchronous client")
        client = AsyncClient()
        for name, kwargs in funcs_to_test:
            print(f"- testing {name}(**{kwargs})")
            func = getattr(client, name)
            result = await func(**kwargs)
            print(f"{result}")

    import asyncio

    test_sync_client()
    asyncio.run(test_async_client())
