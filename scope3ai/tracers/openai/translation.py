import logging
import time
from typing import Any, Callable, Optional, Union

import tiktoken
from openai.resources.audio.translations import AsyncTranslations, Translations
from openai.types.audio.translation import Translation as _Translation
from openai.types.audio.translation_verbose import (
    TranslationVerbose as _TranslationVerbose,
)

from scope3ai.api.types import ImpactRow, Model, Scope3AIContext, Task
from scope3ai.constants import PROVIDERS
from scope3ai.lib import Scope3AI

from .utils import _get_file_audio_duration

PROVIDER = PROVIDERS.OPENAI.value

logger = logging.getLogger(__name__)


class AnnotatedStr(str):
    scope3ai: Optional[Scope3AIContext] = None


class Translation(_Translation):
    scope3ai: Optional[Scope3AIContext] = None


class TranslationVerbose(_TranslationVerbose):
    scope3ai: Optional[Scope3AIContext] = None


def _openai_translation_wrapper(
    response: Any, request_latency: float, kwargs: dict
) -> Union[Translation, TranslationVerbose, AnnotatedStr]:
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
        options["input_audio_seconds"] = int(duration)

    scope3_row = ImpactRow(
        model=Model(id=model),
        provider=PROVIDER,
        output_tokens=output_tokens,
        request_duration_ms=request_latency,
        task=Task.translation,
        **options,
    )
    scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)

    if isinstance(response, _Translation):
        result = Translation.model_construct(**response.model_dump())
    elif isinstance(response, _TranslationVerbose):
        result = TranslationVerbose.model_construct(**response.model_dump())
    elif isinstance(response, str):
        result = AnnotatedStr(str)
    else:
        logger.error(f"Unexpected response type: {type(response)}")
        return response
    result.scope3ai = scope3_ctx
    return result


def openai_translation_wrapper(
    wrapped: Callable, instance: Translations, args: Any, kwargs: Any
) -> Union[Translation, TranslationVerbose, AnnotatedStr]:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = (time.perf_counter() - timer_start) * 1000
    return _openai_translation_wrapper(response, request_latency, kwargs)


async def openai_async_translation_wrapper(
    wrapped: Callable, instance: AsyncTranslations, args: Any, kwargs: Any
) -> Union[Translation, TranslationVerbose, AnnotatedStr]:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = (time.perf_counter() - timer_start) * 1000
    return _openai_translation_wrapper(response, request_latency, kwargs)
