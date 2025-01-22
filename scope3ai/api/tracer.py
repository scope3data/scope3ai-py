from typing import List, Optional

from .typesgen import ImpactResponse, ModeledRow


class Tracer:
    def __init__(
        self,
        name: str = None,
        keep_traces: bool = False,
    ) -> None:
        from scope3ai.lib import Scope3AI

        self.scope3ai = Scope3AI.get_instance()
        self.name = name
        self.keep_traces = keep_traces
        self.children: List[Tracer] = []
        self.rows: List[ModeledRow] = []
        self.traces = []  # type: List[Scope3AIContext]

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
