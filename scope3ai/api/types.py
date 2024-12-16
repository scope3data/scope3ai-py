from pydantic import BaseModel, Field
from typing import Optional

from .typesgen import (
    StatusResponse,
    ImpactBigQueryRequest,
    ImpactBigQueryResponse,
    ImpactBigQueryError,
    ImpactMetrics,
    PredictionStep,
    Details,
    Error,
    GPU,
    ManagedServiceProvider,
    Image,
    CloudProvider,
    Task,
    Family,
    DataType,
    CountryCode,
    RegionCode,
    GPUResponse,
    ImpactLogRow,
    Model,
    GridMix,
    Node,
    ModelResponse,
    NodeResponse,
    ImpactLogRequest,
    ImpactRow,
    DebugInfo,
    ImpactRequest,
    ModeledRow,
    ImpactResponse,
)


class Scope3AIContext(BaseModel):
    request: Optional[ImpactRow] = Field(
        None,
        description="The impact request information. Contains `trace_id` and `record_id`",
    )
    impact: Optional[ModeledRow] = Field(
        None,
        description="The impact response if `include_impact_response` is set to True",
    )


__all__ = [
    "Scope3AIContext",
    "StatusResponse",
    "ImpactBigQueryRequest",
    "ImpactBigQueryResponse",
    "ImpactBigQueryError",
    "ImpactMetrics",
    "PredictionStep",
    "Details",
    "Error",
    "GPU",
    "ManagedServiceProvider",
    "Image",
    "CloudProvider",
    "Task",
    "Family",
    "DataType",
    "CountryCode",
    "RegionCode",
    "GPUResponse",
    "ImpactLogRow",
    "Model",
    "GridMix",
    "Node",
    "ModelResponse",
    "NodeResponse",
    "ImpactLogRequest",
    "ImpactRow",
    "DebugInfo",
    "ImpactRequest",
    "ModeledRow",
    "ImpactResponse",
]
