from os import getenv
from typing import Optional, TypeVar

import httpx
from pydantic import BaseModel

from .commandsgen import ClientCommands
from .defaults import DEFAULT_API_URL

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
