from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Callable, Optional, Union

from huggingface_hub import InferenceClient  # type: ignore[import-untyped]
from huggingface_hub import TextToImageOutput as _TextToImageOutput

from scope3ai.api.types import Scope3AIContext


@dataclass
class TextToImageOutput(_TextToImageOutput):
    scope3ai: Optional[Scope3AIContext] = None


def huggingface_text_to_image_wrapper_stream(**kwargs):
    return TextToImageOutput()


def huggingface_text_to_image_wrapper_non_stream(**kwargs):
    return TextToImageOutput()


def huggingface_text_to_image_wrapper(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> Union[TextToImageOutput, Iterable[TextToImageOutput]]:
    if kwargs.get("stream", False):
        print(kwargs)
        return huggingface_text_to_image_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return huggingface_text_to_image_wrapper_non_stream(
            wrapped, instance, args, kwargs
        )
