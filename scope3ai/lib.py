import importlib.metadata
import importlib.util
import logging
from contextlib import contextmanager
from contextvars import ContextVar
from functools import partial
from os import getenv
from typing import Optional
from uuid import UUID, uuid4
import atexit

import httpx

from .types import ImpactRequestRow, ImpactResponse, Scope3AIContext
from .worker import BackgroundWorker

logger = logging.getLogger("scope3ai.lib")


def init_openai_instrumentor() -> None:
    if importlib.util.find_spec("openai") is not None:
        from scope3ai.tracers.openai_tracer import OpenAIInstrumentor

        instrumentor = OpenAIInstrumentor()
        instrumentor.instrument()


_INSTRUMENTS = {
    "openai": init_openai_instrumentor,
}


class Scope3AIError(Exception):
    pass


class Scope3AITracer:
    def __init__(self) -> None:
        self.scope3ai = Scope3AI.get_instance()
        self.trace_id = uuid4()

    def impact(self) -> ImpactResponse:
        return self.scope3ai.impact(trace_id=self.trace_id, record_id=None)

    async def aimpact(self) -> ImpactResponse:
        return await self.scope3ai.aimpact(trace_id=self.trace_id, record_id=None)


class Scope3AI:
    _instance: Optional["Scope3AI"] = None
    _tracer: ContextVar[list[Scope3AITracer]] = ContextVar("tracer", default=[])
    _worker: Optional[BackgroundWorker] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Scope3AI, cls).__new__(cls)
        return cls._instance

    @classmethod
    def init(
        cls,
        api_key: str = None,
        api_url: str = "https://aiapi.scope3.com/v1",
        include_impact_response: bool = False,
        enable_debug_logging: bool = False,
        providers: list[str] | None = None,
    ) -> None:
        if cls._instance is not None:
            raise Scope3AIError("Scope3AI is already initialized")
        cls._instance = self = Scope3AI()
        self.api_key = api_key or getenv("SCOPE3AI_API_KEY")
        self.api_url = api_url or getenv("SCOPE3AI_API_URL")
        self.include_impact_response = include_impact_response or bool(
            getenv("SCOPE3AI_INCLUDE_IMPACT_RESPONSE", False)
        )
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

        if enable_debug_logging:
            self._init_logging()

        if providers is None:
            providers = list(_INSTRUMENTS.keys())

        http_client_options = {
            "base_url": self.api_url,
            "headers": {"Authorization": f"Bearer {self.api_key}"},
        }
        self._sync_client = httpx.Client(**http_client_options)
        self._async_client = httpx.AsyncClient(**http_client_options)
        self._init_providers(providers)
        self._init_atexit()
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    def impact(
        self,
        trace_id: UUID | None = None,
        record_id: UUID | None = None,
    ) -> ImpactResponse:
        pass

    async def aimpact(
        self,
        trace_id: UUID | None = None,
        record_id: UUID | None = None,
    ) -> ImpactResponse:
        pass

    def submit_impact(
        self,
        impact_request_row: ImpactRequestRow,
    ) -> Scope3AIContext:
        self._ensure_worker()

        def submit_impact(impact_request_row: ImpactRequestRow) -> ImpactResponse:
            req = self._sync_client.post(
                "/impact",
                json=impact_request_row.model_dump(mode="json"),
            )
            return ImpactResponse.parse_obj(req.json())

        ctx = Scope3AIContext(request=impact_request_row)

        if self.include_impact_response:
            impact = submit_impact(impact_request_row)
            ctx.impact = impact
            return ctx

        self._worker.submit(
            partial(submit_impact, impact_request_row=impact_request_row)
        )
        return ctx

    async def asubmit_impact(
        self,
        impact_request_row: ImpactRequestRow,
    ) -> Scope3AIContext:
        self._ensure_worker()
        if self.include_impact_response:
            impact = await self._worker.asubmit_impact(impact_request_row, sync=True)
        else:
            impact = None
            self._worker.submit_impact(impact_request_row)
        return Scope3AIContext(request=impact_request_row, impact=impact)

    def _push_tracer(self, tracer: Scope3AITracer) -> None:
        self._tracer.get().append(tracer)

    def _pop_tracer(self, tracer: Scope3AITracer) -> None:
        self._tracer.get().remove(tracer)

    @property
    def current_tracer(self):
        return self._tracer.get()[-1]

    @contextmanager
    def trace(self):
        tracer = Scope3AITracer()
        try:
            self._push_tracer(tracer)
            yield tracer
        finally:
            self._pop_tracer(tracer)

    def _init_providers(self, providers: list[str]) -> None:
        """Initialize the specified providers."""
        for provider in providers:
            if provider not in _INSTRUMENTS:
                raise Scope3AIError(
                    f"Could not find tracer for the `{provider}` provider."
                )
            init_func = _INSTRUMENTS[provider]
            init_func()

    def _ensure_worker(self) -> None:
        if not self._worker:
            self._worker = BackgroundWorker(-1)

    def _init_logging(self) -> None:
        logging.basicConfig(
            level=logging.INFO,  # Set default logging level to INFO
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Define log format
            handlers=[
                logging.StreamHandler()  # Output logs to the console
            ],
        )
        logging.getLogger("scope3ai").setLevel(logging.DEBUG)

    def _init_atexit(self):
        @atexit.register
        def _shutdown():
            scope3ai = Scope3AI.get_instance()
            logging.debug("Waiting background informations to be processed")
            scope3ai._worker._queue.join()
            logging.debug("Shutting down Scope3AI")
