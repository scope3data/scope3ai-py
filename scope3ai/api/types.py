import asyncio
import threading
from time import monotonic
from typing import Optional

from pydantic import BaseModel, Field, PrivateAttr

from .tracer import Tracer
from .typesgen import (
    GPU,
    CountryCode,
    DataType,
    DebugInfo,
    Details,
    Error,
    Family,
    GPUResponse,
    GridMix,
    Image,
    ImpactBigQueryError,
    ImpactBigQueryRequest,
    ImpactBigQueryResponse,
    ImpactMetrics,
    ImpactRequest,
    ImpactResponse,
    ImpactRow,
    Model,
    ModeledRow,
    ModelResponse,
    Node,
    NodeResponse,
    PredictionStep,
    RegionCode,
    StatusResponse,
    Task,
)


class Scope3AIContext(BaseModel):
    request: Optional[ImpactRow] = Field(
        None,
        description="The impact request information. Contains `trace_id` and `record_id`",
    )
    impact: Optional[ModeledRow] = Field(
        None,
        description=(
            "The impact response. Use `wait_impact` to wait for the "
            "response, or configure `scope3.sync_mode` to True"
        ),
    )

    # non serializable fields
    _tracer: Optional[Tracer] = PrivateAttr(None)
    _impact_sync_ev: threading.Event = PrivateAttr(default_factory=threading.Event)

    def set_impact(self, impact: ModeledRow):
        self.impact = impact
        self._impact_sync_ev.set()
        if self._tracer:
            self._tracer.add_impact(impact)

    def wait_impact(self, timeout: Optional[float] = None):
        self._impact_sync_ev.wait(timeout)
        if not self._impact_sync_ev.is_set():
            raise TimeoutError()
        return self.impact

    async def await_impact(self, timeout: Optional[float] = None):
        # check if the impact is already set, with polling.
        # XXX i have not be able to have a proper async interface
        # without complexify the code.
        start_time = monotonic()
        while not self._impact_sync_ev.is_set():
            elapsed_time = monotonic() - start_time
            if timeout is not None and elapsed_time >= timeout:
                raise asyncio.TimeoutError()
            await asyncio.sleep(0.1)
        return self.impact


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
    "Image",
    "Task",
    "Family",
    "DataType",
    "CountryCode",
    "RegionCode",
    "GPUResponse",
    "Model",
    "GridMix",
    "Node",
    "ModelResponse",
    "NodeResponse",
    "ImpactRow",
    "DebugInfo",
    "ImpactRequest",
    "ModeledRow",
    "ImpactResponse",
]
