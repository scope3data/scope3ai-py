from os import getenv
from typing import Any, List, Optional, TypeVar

import httpx
from pydantic import BaseModel

from .defaults import DEFAULT_API_URL
from .types import (
    Family,
    GPUResponse,
    ImpactRequest,
    ImpactResponse,
    ImpactRow,
    ModelResponse,
    NodeResponse,
)

ClientType = TypeVar("ClientType", httpx.Client, httpx.AsyncClient)


class Scope3AIError(Exception):
    pass


class ClientBase:
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
    ) -> None:
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
    def client(self) -> ClientType:
        """
        Obtain an httpx client for synchronous or asynchronous operation
        with the necessary authentication headers included.
        """
        if not hasattr(self, "_client"):
            self._client = self.create_client()
        return self._client

    def create_client(self) -> ClientType:
        raise NotImplementedError


class ClientCommands:
    def execute_request(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def model(
        self,
        family: Optional[Family] = None,
        with_response: Optional[bool] = True,
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
            with_response=with_response,
        )

    def gpu(
        self,
        with_response: Optional[bool] = True,
    ) -> GPUResponse:
        """
        List GPUs
        """
        return self.execute_request(
            "/gpu",
            method="GET",
            response_model=GPUResponse,
            with_response=with_response,
        )

    def node(
        self,
        service: Optional[str] = None,
        cloud: Optional[str] = None,
        custom: Optional[bool] = None,
        gpu: Optional[str] = None,
        instance: Optional[str] = None,
        with_response: Optional[bool] = True,
    ) -> NodeResponse:
        """
        List nodes
        """
        params = {}
        if service is not None:
            params["service"] = service
        if cloud is not None:
            params["cloud"] = cloud
        if custom is not None:
            params["custom"] = custom
        if gpu is not None:
            params["gpu"] = gpu
        if instance is not None:
            params["instance"] = instance
        return self.execute_request(
            "/node",
            method="GET",
            params=params,
            response_model=NodeResponse,
            with_response=with_response,
        )

    def impact(
        self,
        rows: List[ImpactRow],
        debug: Optional[bool] = None,
        with_response: Optional[bool] = True,
    ) -> ImpactResponse:
        """
        Get impact metrics for a task
        """
        params = {}
        if debug is not None:
            params["debug"] = debug
        json_body = ImpactRequest(rows=rows).model_dump(
            mode="json",
            exclude_unset=True,
        )
        return self.execute_request(
            "/v1/impact",
            method="POST",
            params=params,
            json=json_body,
            response_model=ImpactResponse,
            with_response=with_response,
        )


class Client(ClientBase, ClientCommands):
    """
    Synchronous Client to the Scope3AI HTTP API
    """

    def create_client(self) -> httpx.Client:
        return httpx.Client(headers={"Authorization": f"Bearer {self.api_key}"})

    def execute_request(
        self,
        url: str,
        method="GET",
        params: Optional[dict] = None,
        json: Optional[dict] = None,
        response_model: Optional[BaseModel] = None,
        with_response: Optional[bool] = True,
    ):
        full_url = self.api_url + url
        kwargs = {}
        if params:
            kwargs["params"] = params
        if json:
            kwargs["json"] = json
        response = self.client.request(method, full_url, **kwargs)
        response.raise_for_status()
        if not with_response:
            return
        if response_model:
            return response_model.model_validate(response.json())
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
        with_response: Optional[bool] = True,
    ):
        full_url = self.api_url + url
        kwargs = {}
        if params:
            kwargs["params"] = params
        if json:
            kwargs["json"] = json
        response = await self.client.request(method, full_url, **kwargs)
        response.raise_for_status()
        if not with_response:
            return
        if response_model:
            return response_model.model_validate(response.json())
        return response.json()
