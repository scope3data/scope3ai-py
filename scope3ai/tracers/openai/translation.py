import logging
import time
from typing import Any, Callable, Optional, Union, Tuple

import tiktoken
from openai.resources.audio.translations import AsyncTranslations, Translations
from openai.types.audio.translation import Translation as _Translation
from openai.types.audio.translation_verbose import (
    TranslationVerbose as _TranslationVerbose,
)

from scope3ai.api.types import ImpactRow, Scope3AIContext, Task
from scope3ai.constants import PROVIDERS
from scope3ai.lib import Scope3AI
from scope3ai.tracers.openai.utils import BaseModelResponse
from scope3ai.tracers.utils.audio import _get_file_audio_duration

PROVIDER = PROVIDERS.OPENAI.value
logger = logging.getLogger(__name__)


class AnnotatedStr(str):
    scope3ai: Optional[Scope3AIContext] = None


class Translation(BaseModelResponse, _Translation):
    scope3ai: Optional[Scope3AIContext] = None


class TranslationVerbose(BaseModelResponse, _TranslationVerbose):
    scope3ai: Optional[Scope3AIContext] = None


def _openai_translation_get_impact_row(
    response: Any, request_latency: float, kwargs: dict
) -> Tuple[Union[Translation, TranslationVerbose, AnnotatedStr], ImpactRow]:
    model = kwargs["model"]
    encoder = tiktoken.get_encoding("cl100k_base")

    if isinstance(response, (_Translation, _TranslationVerbose)):
        output_tokens = len(encoder.encode(response.text))
    elif isinstance(response, str):
        output_tokens = len(encoder.encode(response))
    else:
        output_tokens = None

    options = {}
    duration = _get_file_audio_duration(kwargs["file"])
    if duration is not None:
        options["input_audio_seconds"] = duration

    scope3_row = ImpactRow(
        model_id=model,
        managed_service_id=PROVIDER,
        output_tokens=output_tokens,
        request_duration_ms=request_latency,
        task=Task.translation,
        **options,
    )

    if isinstance(response, _Translation):
        result = Translation.model_construct(**response.model_dump())
    elif isinstance(response, _TranslationVerbose):
        result = TranslationVerbose.model_construct(**response.model_dump())
    elif isinstance(response, str):
        result = AnnotatedStr(str)
    else:
        logger.error(f"Unexpected response type: {type(response)}")
        return response, scope3_row
    return result, scope3_row


def openai_translation_wrapper(
    wrapped: Callable, instance: Translations, args: Any, kwargs: Any
) -> Union[Translation, TranslationVerbose, AnnotatedStr]:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = (time.perf_counter() - timer_start) * 1000
    result, impact_row = _openai_translation_get_impact_row(
        response, request_latency, kwargs
    )
    scope3_ctx = Scope3AI.get_instance().submit_impact(impact_row)
    result.scope3ai = scope3_ctx
    return result


async def openai_async_translation_wrapper(
    wrapped: Callable, instance: AsyncTranslations, args: Any, kwargs: Any
) -> Union[Translation, TranslationVerbose, AnnotatedStr]:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = (time.perf_counter() - timer_start) * 1000
    result, impact_row = _openai_translation_get_impact_row(
        response, request_latency, kwargs
    )
    scope3_ctx = await Scope3AI.get_instance().asubmit_impact(impact_row)
    result.scope3ai = scope3_ctx
    return result
