from typing import List, Optional
from uuid import uuid4

from .typesgen import ImpactResponse, ModeledRow


# TODO Tracer is not BaseTracer?
class Tracer:
    """
    Tracer is responsible for tracking and aggregating environmental impact metrics
    from AI model interactions. It supports nested tracing, async operations, and
    provides detailed impact breakdowns for energy, emissions and water usage.

    Args:
        name (str, optional): Name identifier for the tracer. Defaults to None.
        keep_traces (bool, optional): Whether to keep trace history after completion.
            Defaults to False.
        client_id (str, optional): Client identifier for categorizing traces.
            Overrides global `SCOPE3AI_CLIENT_ID` setting. Defaults to None.
        project_id (str, optional): Project identifier for categorizing traces.
            Overrides global `SCOPE3AI_PROJECT_ID` setting. Defaults to None.
        application_id (str, optional): Application identifier for categorizing traces.
            Overrides global `SCOPE3AI_APPLICATION_ID` setting. Defaults to None.
        session_id (str, optional): Session identifier for tracking user sessions.
            Only available at tracer level. Defaults to None.
        trace_id (str, optional): Unique identifier for the trace.
            Auto-generated if not provided. Defaults to None.
    """

    def __init__(
        self,
        name: str = None,
        keep_traces: bool = False,
        client_id: Optional[str] = None,
        project_id: Optional[str] = None,
        application_id: Optional[str] = None,
        session_id: Optional[str] = None,
        trace_id: Optional[str] = None,
    ) -> None:
        from scope3ai.lib import Scope3AI

        self.trace_id = trace_id or uuid4().hex
        self.scope3ai = Scope3AI.get_instance()
        self.name = name
        self.keep_traces = keep_traces
        self.children: List[Tracer] = []
        self.rows: List[ModeledRow] = []
        self.traces = []  # type: List[Scope3AIContext]

        self.client_id = client_id
        self.project_id = project_id
        self.application_id = application_id
        self.session_id = session_id

    def impact(self, timeout: Optional[int] = None) -> ImpactResponse:
        """
        Return an aggregated impact response for the current tracer and its children.

        As the impact is computed asynchronously, this method will wait for the
        impact response to be available before returning it.
        """
        for trace in self.traces:
            trace.wait_impact(timeout)
        return self._impact()

    async def aimpact(self, timeout: Optional[int] = None) -> ImpactResponse:
        """
        Async version of Tracer::impact.
        """
        for trace in self.traces:
            await trace.await_impact(timeout)
        return self._impact()

    def _impact(self) -> ImpactResponse:
        """
        Return an aggregated impact response for the current tracer and its children.
        """
        all_rows = self.get_all_rows()
        return ImpactResponse(
            rows=all_rows,
            total_energy_wh=sum([row.total_impact.usage_energy_wh for row in all_rows]),
            total_gco2e=sum(
                [row.total_impact.usage_emissions_gco2e for row in all_rows]
            ),
            total_mlh2o=sum([row.total_impact.usage_water_ml for row in all_rows]),
            has_errors=any([row.error is not None for row in all_rows]),
        )

    def add_impact(self, impact: ModeledRow) -> None:
        self.rows.append(impact)

    def get_all_rows(self) -> List[ModeledRow]:
        all_rows = self.rows[:]
        for child in self.children:
            all_rows.extend(child.get_all_rows())
        return all_rows

    def _link_parent(self, parent: Optional["Tracer"]) -> None:
        if parent and (self not in parent.children):
            parent.children.append(self)

    def _unlink_parent(self, parent: Optional["Tracer"]) -> None:
        pass

    def _link_trace(self, trace) -> None:
        if trace not in self.traces:
            self.traces.append(trace)

    def _unlink_trace(self, trace) -> None:
        if self.keep_traces:
            return
        if trace in self.traces:
            self.traces.remove(trace)
