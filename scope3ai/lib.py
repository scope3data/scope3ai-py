import importlib.metadata
import importlib.util
import logging
from contextlib import contextmanager
from contextvars import ContextVar
from functools import partial
from os import getenv
from typing import Optional, List
from uuid import uuid4
import atexit

from .api.client import Client, AsyncClient
from .api.types import ImpactRow, ImpactResponse, Scope3AIContext
from .api.defaults import DEFAULT_API_URL
from .worker import BackgroundWorker

logger = logging.getLogger("scope3ai.lib")


def init_openai_instrumentor() -> None:
    if importlib.util.find_spec("openai") is not None:
        from scope3ai.tracers.openai_tracer import OpenAIInstrumentor

        instrumentor = OpenAIInstrumentor()
        instrumentor.instrument()


def init_hugginface_hub_instrumentor() -> None:
    if importlib.util.find_spec("huggingface_hub") is not None:
        from scope3ai.tracers.huggingface.huggingface_tracer import (
            HuggingfaceInstrumentor,
        )

        instrumentor = HuggingfaceInstrumentor()
        instrumentor.instrument()


_INSTRUMENTS = {
    "openai": init_openai_instrumentor,
    "huggingface_hub": init_hugginface_hub_instrumentor,
}


def generate_id() -> str:
    return uuid4().hex


class Scope3AIError(Exception):
    pass


class Tracer:
    def __init__(
        self,
        name: str = None,
        trace_id: str = None,
        parent_trace_id: str = None,
        session_id: str = None,
    ) -> None:
        self.scope3ai = Scope3AI.get_instance()
        if trace_id is None:
            trace_id = generate_id()
        self.trace_id = trace_id
        self.session_id = None
        self.parent_trace_id = None
        self.name = name

    def impact(self) -> ImpactResponse:
        return self.scope3ai.impact(trace_id=self.trace_id)

    async def aimpact(self) -> ImpactResponse:
        return await self.scope3ai.aimpact(trace_id=self.trace_id)

    def _link_parent(self, tracer: Optional["Tracer"] = None):
        if self.parent_trace_id is None and tracer:
            self.parent_trace_id = tracer.trace_id

    def _unlink_parent(self, tracer: Optional["Tracer"] = None):
        if tracer and tracer.trace_id == self.parent_trace_id:
            self.parent_trace_id = None


class Scope3AI:
    """
    Scope3AI tracer class

    This class is a singleton that provides a context manager for tracing
    inference metadata and submitting impact requests to the Scope3 AI API.
    """

    _instance: Optional["Scope3AI"] = None
    _tracer: ContextVar[List[Tracer]] = ContextVar("tracer", default=[])
    _worker: Optional[BackgroundWorker] = None
    _providers: List[str] = []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Scope3AI, cls).__new__(cls)
        return cls._instance

    @classmethod
    def init(
        cls,
        api_key: str = None,
        api_url: str = None,
        include_impact_response: bool = False,
        enable_debug_logging: bool = False,
        providers: Optional[List[str]] = None,
    ) -> None:
        if cls._instance is not None:
            raise Scope3AIError("Scope3AI is already initialized")
        cls._instance = self = Scope3AI()
        self.api_key = api_key or getenv("SCOPE3AI_API_KEY")
        self.api_url = api_url or getenv("SCOPE3AI_API_URL") or DEFAULT_API_URL
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

        http_client_options = {"api_key": self.api_key, "api_url": self.api_url}
        self._sync_client = Client(**http_client_options)
        self._async_client = AsyncClient(**http_client_options)
        self._init_providers(providers)
        self._init_atexit()
        return cls._instance

    @classmethod
    def get_instance(cls) -> "Scope3AI":
        """
        Return the instance of the Scope3AI singleton.

        This method provides access to the default global state of the
        Scope3AI library. The returned instance can be used to trace
        inference metadata and submit impact requests to the Scope3 AI
        API from anywhere in the application.

        Returns:
            Scope3AI: The singleton instance of the Scope3AI class.
        """
        return cls._instance

    def impact(
        self,
        session_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        record_id: Optional[str] = None,
    ) -> ImpactResponse:
        pass

    async def aimpact(
        self,
        session_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        record_id: Optional[str] = None,
    ) -> ImpactResponse:
        pass

    def submit_impact(
        self,
        impact_row: ImpactRow,
    ) -> Scope3AIContext:
        """
        Submit an impact request to the Scope3 AI API.

        This function sends an impact request represented by the `impact_row`
        to the Scope3 AI API and optionally returns the response.

        Args:
            impact_row (ImpactRow): The impact request data
                that needs to be submitted to the Scope3 AI API.

        Returns:
            Scope3AIContext: A context object containing the request data and
            optionally the response from the API if `include_impact_response`
            is set to True.
        """

        def submit_impact(
            impact_row: ImpactRow,
            with_response=True,
        ) -> Optional[ImpactResponse]:
            return self._sync_client.impact(
                rows=[impact_row],
                with_response=with_response,
            )

        self._mark_impact_row(impact_row)
        ctx = Scope3AIContext(request=impact_row)

        if self.include_impact_response:
            response = submit_impact(impact_row, with_response=True)
            ctx.impact = response.rows[0]
            return ctx

        self._ensure_worker()
        self._worker.submit(partial(submit_impact, impact_row=impact_row))
        return ctx

    async def asubmit_impact(
        self,
        impact_row: ImpactRow,
    ) -> Scope3AIContext:
        """
        Async version of Scope3AI::submit_impact.
        """

        async def submit_impact(
            impact_row: ImpactRow,
            with_response=True,
        ) -> Optional[ImpactResponse]:
            return await self._async_client.impact(
                rows=[impact_row],
                with_response=with_response,
            )

        self._mark_impact_row(impact_row)
        ctx = Scope3AIContext(request=impact_row)

        if self.include_impact_response:
            impact = await submit_impact(impact_row, with_response=True)
            ctx.impact = impact
            return ctx

        self._ensure_worker()
        self._worker.submit(partial(submit_impact, impact_row=impact_row))
        return ctx

    @property
    def root_tracer(self):
        """
        Return the root tracer.

        The root tracer is the first tracer in the current execution context
        (tracer stack). If no tracers are currently active, it returns None.

        Returns:
            Tracer: The root tracer if available, otherwise None.
        """
        tracers = self._tracer.get()
        return tracers[0] if tracers else None

    @property
    def current_tracer(self):
        """
        Return the current tracer.

        The current tracer is the last tracer in the current execution context
        (tracer stack). If no tracers are currently active, it returns None.

        Returns:
            Tracer: The current tracer if available, otherwise None.
        """
        tracers = self._tracer.get()
        return tracers[-1] if tracers else None

    @contextmanager
    def trace(self):
        tracer = Tracer()
        try:
            self._push_tracer(tracer)
            yield tracer
        finally:
            self._pop_tracer(tracer)

    def close(self):
        if self._worker:
            self._worker.kill()
        self.__class__._instance = None

    #
    # Internals
    #

    def _push_tracer(self, tracer: Tracer) -> None:
        tracer._link_parent(self.current_tracer)
        self._tracer.get().append(tracer)

    def _pop_tracer(self, tracer: Tracer) -> None:
        self._tracer.get().remove(tracer)
        tracer._unlink_parent(self.current_tracer)

    def _init_providers(self, providers: List[str]) -> None:
        """Initialize the specified providers."""
        for provider in providers:
            if provider not in _INSTRUMENTS:
                raise Scope3AIError(
                    f"Could not find tracer for the `{provider}` provider."
                )
            if provider in self._providers:
                # already initialized
                continue
            init_func = _INSTRUMENTS[provider]
            init_func()
            self._providers.append(provider)

    def _ensure_worker(self) -> None:
        if not self._worker:
            self._worker = BackgroundWorker(-1)

    def _init_logging(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
        )
        logging.getLogger("scope3ai").setLevel(logging.DEBUG)

    def _init_atexit(self):
        @atexit.register
        def _shutdown():
            # do not reinstanciate the singleton here if somehow it was deleted
            scope3ai = Scope3AI._instance
            if not scope3ai:
                return
            if scope3ai._worker and scope3ai._worker._queue:
                logging.debug("Waiting background informations to be processed")
                scope3ai._worker._queue.join()
                logging.debug("Shutting down Scope3AI")

    def _mark_impact_row(self, impact_row: ImpactRow) -> None:
        # augment the impact_row with the current information from the tracer
        impact_row.request_id = generate_id()
        current_tracer = self.current_tracer
        if current_tracer:
            impact_row.trace_id = current_tracer.trace_id
            impact_row.parent_trace_id = current_tracer.parent_trace_id
        root_tracer = self.root_tracer
        if root_tracer:
            impact_row.session_id = root_tracer.session_id
