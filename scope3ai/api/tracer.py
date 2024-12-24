from typing import List, Optional
from .typesgen import ImpactResponse, ModeledRow, ImpactMetrics


class Tracer:
    def __init__(
        self,
        name: str = None,
    ) -> None:
        from scope3ai.lib import Scope3AI

        self.scope3ai = Scope3AI.get_instance()
        self.name = name
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

    def _sum_modeled_rows(self, rows: List[ModeledRow]) -> ModeledRow:
        if not rows:
            raise Exception("No rows to sum")
        result = ModeledRow(
            inference_impact=self._sum_impact_metrics(
                [row.inference_impact for row in rows]
            ),
            training_impact=self._sum_impact_metrics(
                [row.training_impact for row in rows]
            ),
            fine_tuning_impact=self._sum_impact_metrics(
                [row.fine_tuning_impact for row in rows]
            ),
            total_impact=self._sum_impact_metrics([row.total_impact for row in rows]),
        )
        return result

    def _sum_impact_metrics(self, metrics: List[ImpactMetrics]) -> ImpactMetrics:
        # Initialize totals
        total_usage_energy_wh = 0.0
        total_usage_emissions_gco2e = 0.0
        total_usage_water_ml = 0.0
        total_embodied_emissions_gco2e = 0.0
        total_embodied_water_ml = 0.0

        # Aggregate values
        for metric in metrics:
            if not isinstance(metric, ImpactMetrics):
                raise TypeError(
                    "All items in the list must be instances of ImpactMetrics."
                )
            total_usage_energy_wh += metric.usage_energy_wh
            total_usage_emissions_gco2e += metric.usage_emissions_gco2e
            total_usage_water_ml += metric.usage_water_ml
            total_embodied_emissions_gco2e += metric.embodied_emissions_gco2e
            total_embodied_water_ml += metric.embodied_water_ml

        # Return a new instance with summed values
        return ImpactMetrics(
            usage_energy_wh=total_usage_energy_wh,
            usage_emissions_gco2e=total_usage_emissions_gco2e,
            usage_water_ml=total_usage_water_ml,
            embodied_emissions_gco2e=total_embodied_emissions_gco2e,
            embodied_water_ml=total_embodied_water_ml,
        )

    def _link_parent(self, parent: Optional["Tracer"]) -> None:
        if parent and (self not in parent.children):
            parent.children.append(self)

    def _unlink_parent(self, parent: Optional["Tracer"]) -> None:
        pass

    def _link_trace(self, trace) -> None:
        if trace not in self.traces:
            self.traces.append(trace)

    def _unlink_trace(self, trace) -> None:
        if trace in self.traces:
            self.traces.remove(trace)
