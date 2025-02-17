# generated by generate-client-commands.py
#  filename: aiapi.yaml
#  timestamp: 2025-02-05T23:50:37+00:00

from typing import Any, Optional

from .typesgen import (
    GPU,
    Family,
    GPUCreateRequest,
    GPUResponse,
    GPUUpdateRequest,
    ImpactBigQueryRequest,
    ImpactBigQueryResponse,
    ImpactRequest,
    ImpactResponse,
    Model,
    ModelCreateRequest,
    ModelResponse,
    ModelUpdateRequest,
    Node,
    NodeCreateRequest,
    NodeResponse,
    NodeUpdateRequest,
    StatusResponse,
)


class ClientCommands:
    """
    Base class that implements the command methods for interacting with the Scope3AI API.
    The execute_request method must be implemented by subclasses to handle the actual HTTP requests.
    """

    def execute_request(self, *args, **kwargs) -> Any:
        """
        Execute an HTTP request to the Scope3AI API.
        Must be implemented by subclasses to handle synchronous or asynchronous requests.
        """
        raise NotImplementedError

    def status(self, with_response: Optional[bool] = True) -> StatusResponse:
        """ """
        return self.execute_request(
            "/status",
            method="GET",
            response_model=StatusResponse,
            with_response=with_response,
        )

    def reload(self, with_response: Optional[bool] = True) -> StatusResponse:
        """ """
        return self.execute_request(
            "/reload",
            method="GET",
            response_model=StatusResponse,
            with_response=with_response,
        )

    def list_models(
        self, family: Optional[Family] = None, with_response: Optional[bool] = True
    ) -> ModelResponse:
        """List models"""
        params = {}
        if family is not None:
            params["family"] = family
        return self.execute_request(
            "/model",
            method="GET",
            params=params,
            response_model=ModelResponse,
            with_response=with_response,
        )

    def create_model(
        self, content: ModelCreateRequest, with_response: Optional[bool] = True
    ) -> Model:
        """Create a model"""
        return self.execute_request(
            "/model",
            method="POST",
            json=content,
            response_model=Model,
            with_response=with_response,
        )

    def get_model(self, model_id: str, with_response: Optional[bool] = True) -> Model:
        """Get a specific model (global or custom)"""
        return self.execute_request(
            "/model/{modelId}",
            method="GET",
            response_model=Model,
            with_response=with_response,
        )

    def update_model(
        self,
        model_id: str,
        content: ModelUpdateRequest,
        with_response: Optional[bool] = True,
    ) -> Model:
        """Update a model"""
        return self.execute_request(
            "/model/{modelId}",
            method="PUT",
            json=content,
            response_model=Model,
            with_response=with_response,
        )

    def delete_model(self, model_id: str, with_response: Optional[bool] = True) -> None:
        """Delete a model"""
        return self.execute_request(
            "/model/{modelId}", method="DELETE", with_response=with_response
        )

    def add_model_alias(
        self, model_id: str, content: dict, with_response: Optional[bool] = True
    ) -> None:
        """Add a new alias to a model"""
        return self.execute_request(
            "/model/{modelId}/alias",
            method="PUT",
            json=content,
            with_response=with_response,
        )

    def remove_model_alias(
        self, model_id: str, alias: str, with_response: Optional[bool] = True
    ) -> None:
        """Remove an alias from a model"""
        return self.execute_request(
            "/model/{modelId}/alias/{alias}",
            method="DELETE",
            with_response=with_response,
        )

    def list_nodes(
        self,
        service: Optional[str] = None,
        cloud: Optional[str] = None,
        custom: Optional[bool] = None,
        gpu: Optional[str] = None,
        instance: Optional[str] = None,
        with_response: Optional[bool] = True,
    ) -> NodeResponse:
        """List nodes (both global and custom)"""
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

    def create_node(
        self, content: NodeCreateRequest, with_response: Optional[bool] = True
    ) -> Node:
        """Create a custom node"""
        return self.execute_request(
            "/node",
            method="POST",
            json=content,
            response_model=Node,
            with_response=with_response,
        )

    def get_node(self, node_id: str, with_response: Optional[bool] = True) -> Node:
        """Get a specific node (global or custom)"""
        return self.execute_request(
            "/node/{nodeId}",
            method="GET",
            response_model=Node,
            with_response=with_response,
        )

    def update_node(
        self,
        node_id: str,
        content: NodeUpdateRequest,
        with_response: Optional[bool] = True,
    ) -> Node:
        """Update a node (custom nodes only, unless admin)"""
        return self.execute_request(
            "/node/{nodeId}",
            method="PUT",
            json=content,
            response_model=Node,
            with_response=with_response,
        )

    def delete_node(self, node_id: str, with_response: Optional[bool] = True) -> None:
        """Delete a node (custom nodes only, unless admin)"""
        return self.execute_request(
            "/node/{nodeId}", method="DELETE", with_response=with_response
        )

    def list_gpus(self, with_response: Optional[bool] = True) -> GPUResponse:
        """List GPUs"""
        return self.execute_request(
            "/gpu",
            method="GET",
            response_model=GPUResponse,
            with_response=with_response,
        )

    def create_gpu(
        self, content: GPUCreateRequest, with_response: Optional[bool] = True
    ) -> GPU:
        """Create a GPU"""
        return self.execute_request(
            "/gpu",
            method="POST",
            json=content,
            response_model=GPU,
            with_response=with_response,
        )

    def get_gpu(self, gpu_id: str, with_response: Optional[bool] = True) -> GPU:
        """Get a specific GPU (global or custom)"""
        return self.execute_request(
            "/gpu/{gpuId}",
            method="GET",
            response_model=GPU,
            with_response=with_response,
        )

    def update_gpu(
        self,
        gpu_id: str,
        content: GPUUpdateRequest,
        with_response: Optional[bool] = True,
    ) -> GPU:
        """Update a GPU"""
        return self.execute_request(
            "/gpu/{gpuId}",
            method="PUT",
            json=content,
            response_model=GPU,
            with_response=with_response,
        )

    def delete_gpu(self, gpu_id: str, with_response: Optional[bool] = True) -> None:
        """Delete a GPU"""
        return self.execute_request(
            "/gpu/{gpuId}", method="DELETE", with_response=with_response
        )

    def get_impact(
        self,
        content: ImpactRequest,
        debug: Optional[bool] = None,
        with_response: Optional[bool] = True,
    ) -> ImpactResponse:
        """Get impact metrics for a task"""
        params = {}
        if debug is not None:
            params["debug"] = debug
        return self.execute_request(
            "/v1/impact",
            method="POST",
            params=params,
            json=content,
            response_model=ImpactResponse,
            with_response=with_response,
        )

    def calculate_impact_big_query(
        self, content: ImpactBigQueryRequest, with_response: Optional[bool] = True
    ) -> ImpactBigQueryResponse:
        """Calculate AI model impact metrics for BigQuery"""
        return self.execute_request(
            "/",
            method="POST",
            json=content,
            response_model=ImpactBigQueryResponse,
            with_response=with_response,
        )
