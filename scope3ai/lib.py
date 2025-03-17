import atexit
import importlib.util
import logging
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
from functools import partial
from os import getenv
from typing import List, Optional
from uuid import uuid4

from .api.client import AsyncClient, Client
from .api.defaults import DEFAULT_API_URL, DEFAULT_APPLICATION_ID
from .api.tracer import Tracer
from .api.types import ImpactRequest, ImpactResponse, ImpactRow, Scope3AIContext
from .constants import CLIENTS
from .worker import BackgroundWorker

logger = logging.getLogger("scope3ai.lib")


def init_anthropic_instrumentor() -> None:
    if importlib.util.find_spec("anthropic") is not None:
        from scope3ai.tracers.anthropic.instrument import AnthropicInstrumentor

        instrumentor = AnthropicInstrumentor()
        instrumentor.instrument()


def init_cohere_instrumentor() -> None:
    if importlib.util.find_spec("cohere") is not None:
        from scope3ai.tracers.cohere.instrument import CohereInstrumentor

        instrumentor = CohereInstrumentor()
        instrumentor.instrument()


def init_openai_instrumentor() -> None:
    if importlib.util.find_spec("openai") is not None:
        from scope3ai.tracers.openai.instrument import OpenAIInstrumentor

        instrumentor = OpenAIInstrumentor()
        instrumentor.instrument()


def init_huggingface_hub_instrumentor() -> None:
    if importlib.util.find_spec("huggingface_hub") is not None:
        from scope3ai.tracers.huggingface.instrument import HuggingfaceInstrumentor

        instrumentor = HuggingfaceInstrumentor()
        instrumentor.instrument()


def init_google_genai_instrumentor() -> None:
    if importlib.util.find_spec("google") is not None:
        from scope3ai.tracers.google_genai.instrument import GoogleGenAiInstrumentor

        instrumentor = GoogleGenAiInstrumentor()
        instrumentor.instrument()


def init_litellm_instrumentor() -> None:
    if importlib.util.find_spec("litellm") is not None:
        from scope3ai.tracers.litellm.instrument import LiteLLMInstrumentor

        instrumentor = LiteLLMInstrumentor()
        instrumentor.instrument()


def init_mistral_v1_instrumentor() -> None:
    if importlib.util.find_spec("mistralai") is not None:
        from scope3ai.tracers.mistralai.instrument import MistralAIInstrumentor

        instrumentor = MistralAIInstrumentor()
        instrumentor.instrument()


def init_response_instrumentor() -> None:
    from scope3ai.response_interceptor.instrument import ResponseInterceptor

    instrumentor = ResponseInterceptor()
    instrumentor.instrument()


_INSTRUMENTS = {
    CLIENTS.ANTHROPIC.value: init_anthropic_instrumentor,
    CLIENTS.COHERE.value: init_cohere_instrumentor,
    CLIENTS.OPENAI.value: init_openai_instrumentor,
    CLIENTS.HUGGINGFACE_HUB.value: init_huggingface_hub_instrumentor,
    # TODO current tests use gemini
    CLIENTS.GOOGLE_OPENAI.value: init_google_genai_instrumentor,
    CLIENTS.LITELLM.value: init_litellm_instrumentor,
    CLIENTS.MISTRALAI.value: init_mistral_v1_instrumentor,
    CLIENTS.RESPONSE.value: init_response_instrumentor,
}

# TODO what it means / why reinit is allowed here
_RE_INIT_CLIENTS = [CLIENTS.RESPONSE.value]


def generate_id() -> str:
    return uuid4().hex


class Scope3AIError(Exception):
    pass


class Scope3AI:
    """
    Scope3AI tracer class

    This class is a singleton that provides a context manager for tracing
    inference metadata and submitting impact requests to the Scope3 AI API.
    """

    _instance: Optional["Scope3AI"] = None
    _tracer: ContextVar[List[Tracer]] = ContextVar("tracer", default=[])
    _worker: Optional[BackgroundWorker] = None
    _clients: List[str] = []
    _keep_tracers: bool = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Scope3AI, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.api_key: Optional[str] = None
        self.api_url: Optional[str] = None
        self.sync_mode: bool = False
        self._sync_client: Optional[Client] = None
        self._async_client: Optional[AsyncClient] = None
        self.environment: Optional[str] = None
        self.client_id: Optional[str] = None
        self.project_id: Optional[str] = None
        self.application_id: Optional[str] = None

    @classmethod
    def init(
        cls,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        sync_mode: bool = False,
        enable_debug_logging: bool = False,
        # we have provider_clients and not clients naming here because client also has client_id which is not a [provider] client but a [scope3] client
        provider_clients: Optional[List[str]] = None,
        # metadata for scope3
        environment: Optional[str] = None,
        client_id: Optional[str] = None,
        project_id: Optional[str] = None,
        application_id: Optional[str] = None,
    ) -> "Scope3AI":
        """
        Initialize the Scope3AI SDK with the provided configuration settings.

        Args:
            api_key (str, optional): The Scope3AI API key. Can be set via `SCOPE3AI_API_KEY`
                environment variable. Required for authentication.
            api_url (str, optional): The base URL for the Scope3AI API. Can be set via
                `SCOPE3AI_API_URL` environment variable. Defaults to standard API URL.
            sync_mode (bool, optional): If True, the SDK will operate synchronously. Can be
                set via `SCOPE3AI_SYNC_MODE` environment variable. Defaults to False.
            enable_debug_logging (bool, optional): Enable debug level logging. Can be set via
                `SCOPE3AI_DEBUG_LOGGING` environment variable. Defaults to False.
            clients (List[str], optional): List of provider clients to instrument. If None,
                all available provider clients will be instrumented.
            environment (str, optional): The environment name (e.g. "production", "staging").
                Can be set via `SCOPE3AI_ENVIRONMENT` environment variable.
            client_id (str, optional): Client identifier for grouping traces. Can be set via
                `SCOPE3AI_CLIENT_ID` environment variable.
            project_id (str, optional): Project identifier for grouping traces. Can be set via
                `SCOPE3AI_PROJECT_ID` environment variable.
            application_id (str, optional): Application identifier. Can be set via
                `SCOPE3AI_APPLICATION_ID` environment variable. Defaults to "default".

        Returns:
            Scope3AI: The initialized Scope3AI instance.

        Raises:
            Scope3AIError: If the instance is already initialized or if required settings are missing.
        """
        if cls._instance is not None:
            raise Scope3AIError("Scope3AI is already initialized")
        cls._instance = self = Scope3AI()
        self.api_key = api_key or getenv("SCOPE3AI_API_KEY")
        self.api_url = api_url or getenv("SCOPE3AI_API_URL") or DEFAULT_API_URL
        self.sync_mode = sync_mode or bool(getenv("SCOPE3AI_SYNC_MODE", False))
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

        # metadata
        self.environment = environment or getenv("SCOPE3AI_ENVIRONMENT")
        self.client_id = client_id or getenv("SCOPE3AI_CLIENT_ID")
        self.project_id = project_id or getenv("SCOPE3AI_PROJECT_ID")
        self.application_id = (
            application_id
            or getenv("SCOPE3AI_APPLICATION_ID")
            or DEFAULT_APPLICATION_ID
        )

        if enable_debug_logging:
            self._init_logging()

        clients = provider_clients
        if clients is None:
            clients = list(_INSTRUMENTS.keys())

        http_client_options = {"api_key": self.api_key, "api_url": self.api_url}
        self._sync_client = Client(**http_client_options)
        self._async_client = AsyncClient(**http_client_options)
        self._init_clients(clients)
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
        if not cls._instance:
            raise Scope3AIError("Scope3AI is not initialized. Use Scope3AI.init()")
        return cls._instance

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
            the response from the API.
        """

        def submit_impact(
            impact_row: ImpactRow,
            ctx: Scope3AIContext,
        ) -> Optional[ImpactResponse]:
            assert self._sync_client is not None
            response = self._sync_client.get_impact(
                content=ImpactRequest(rows=[impact_row]),
                with_response=True,
            )
            ctx.set_impact(response.rows[0])
            if ctx._tracer:
                ctx._tracer._unlink_trace(ctx)
            return response

        tracer = self.current_tracer
        self._fill_impact_row(impact_row, tracer, self.root_tracer)
        ctx = Scope3AIContext(request=impact_row)
        ctx._tracer = tracer
        if tracer:
            tracer._link_trace(ctx)

        if self.sync_mode:
            submit_impact(impact_row, ctx=ctx)
            return ctx

        self._ensure_worker()
        assert self._worker is not None
        self._worker.submit(partial(submit_impact, impact_row=impact_row, ctx=ctx))
        return ctx

    async def asubmit_impact(
        self,
        impact_row: ImpactRow,
    ) -> Scope3AIContext:
        """
        Async version of Scope3AI::submit_impact.
        """

        if not self.sync_mode:
            # in non sync-mode, it uses the background worker,
            # and the background worker is not async (does not have to be).
            # so we just redirect the call to the sync version.
            return self.submit_impact(impact_row)

        tracer = self.current_tracer
        self._fill_impact_row(impact_row, tracer, self.root_tracer)
        ctx = Scope3AIContext(request=impact_row)
        ctx._tracer = tracer
        if tracer:
            tracer._link_trace(ctx)

        assert self._async_client is not None
        response = await self._async_client.get_impact(
            content=ImpactRequest(rows=[impact_row]),
            with_response=True,
        )
        ctx.set_impact(response.rows[0])
        if tracer:
            tracer._unlink_trace(ctx)

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
    def trace(
        self,
        keep_traces=False,
        client_id: Optional[str] = None,
        project_id: Optional[str] = None,
        application_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ):
        root_tracer = self.root_tracer
        if not client_id:
            client_id = root_tracer.client_id if root_tracer else self.client_id
        if not project_id:
            project_id = root_tracer.project_id if root_tracer else self.project_id
        if not application_id:
            application_id = (
                root_tracer.application_id if root_tracer else self.application_id
            )
        if not session_id:
            session_id = root_tracer.session_id if root_tracer else None
        tracer = Tracer(
            keep_traces=keep_traces,
            client_id=client_id,
            project_id=project_id,
            application_id=application_id,
            session_id=session_id,
        )
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

    def _init_clients(self, clients: List[str]) -> None:
        for client in clients:
            if client not in _INSTRUMENTS:
                raise Scope3AIError(f"Could not find tracer for the `{client}` client.")
            if client in self._clients and client not in _RE_INIT_CLIENTS:
                # already initialized
                continue
            init_func = _INSTRUMENTS[client]
            init_func()
            self._clients.append(client)

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

    def _fill_impact_row(
        self,
        row: ImpactRow,
        tracer: Optional[Tracer] = None,
        root_tracer: Optional[Tracer] = None,
    ):
        # fill fields with information we know about
        # One trick is to not set anything on the ImpactRow if it's already set or if the value is None
        # because the model are dumped and exclude the fields unset.
        # If we set a field to None, it will be added for nothing.
        def set_only_if(row, field, *values):
            if getattr(row, field) is not None:
                return
            for value in values:
                if value is not None:
                    setattr(row, field, value)
                    return

        row.request_id = generate_id()
        if root_tracer:
            set_only_if(row, "trace_id", root_tracer.trace_id)
        if row.utc_datetime is None:
            row.utc_datetime = datetime.now(tz=timezone.utc)

        # copy global-only metadata
        set_only_if(
            row,
            "environment",
            self.environment,
        )

        # copy tracer or global metadata

        set_only_if(
            row,
            "managed_service_id",
            row.managed_service_id if row.managed_service_id else "",
        )

        set_only_if(
            row,
            "client_id",
            tracer.client_id if tracer else None,
            self.client_id,
        )
        set_only_if(
            row,
            "project_id",
            tracer.project_id if tracer else None,
            self.project_id,
        )
        set_only_if(
            row,
            "application_id",
            tracer.application_id if tracer else None,
            self.application_id,
        )
        set_only_if(
            row,
            "session_id",
            tracer.session_id if tracer else None,
        )
