import logging
import time
import warnings
from typing import Callable
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Union

from huggingface_hub import InferenceClient
from huggingface_hub.constants import INFERENCE_ENDPOINT
from huggingface_hub.errors import InferenceTimeoutError
from huggingface_hub.inference._common import (
    TASKS_EXPECTING_IMAGES,
    ContentT,
    _open_as_binary,
)
from huggingface_hub.utils import get_session, hf_raise_for_status
from requests import HTTPError

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


def post(
    instance: InferenceClient,
    *,
    json: Optional[Union[str, Dict, List]] = None,
    data: Optional[ContentT] = None,
    model: Optional[str] = None,
    task: Optional[str] = None,
    stream: bool = False,
) -> Union[bytes, Iterable[bytes]]:
    url = instance._resolve_url(model, task)

    if data is not None and json is not None:
        warnings.warn("Ignoring `json` as `data` is passed as binary.")
    headers = instance.headers.copy()
    if task in TASKS_EXPECTING_IMAGES and "Accept" not in headers:
        headers["Accept"] = "image/png"

    t0 = time.time()
    timeout = instance.timeout
    while True:
        with _open_as_binary(data) as data_as_binary:
            try:
                response = get_session().post(
                    url,
                    json=json,
                    data=data_as_binary,
                    headers=headers,
                    cookies=instance.cookies,
                    timeout=instance.timeout,
                    stream=stream,
                    proxies=instance.proxies,
                )
            except TimeoutError as error:
                # Convert any `TimeoutError` to a `InferenceTimeoutError`
                raise InferenceTimeoutError(
                    f"Inference call timed out: {url}"
                ) from error  # type: ignore

        try:
            hf_raise_for_status(response)
            setattr(instance, "response", response)
            return response.iter_lines() if stream else response.content
        except HTTPError as error:
            if error.response.status_code == 422 and task is not None:
                error.args = (
                    f"{error.args[0]}\nMake sure '{task}' task is supported by the model.",
                ) + error.args[1:]
            if error.response.status_code == 503:
                # If Model is unavailable, either raise a TimeoutError...
                if timeout is not None and time.time() - t0 > timeout:
                    raise InferenceTimeoutError(
                        f"Model not loaded on the server: {url}. Please retry with a higher timeout (current:"
                        f" {instance.timeout}).",
                        request=error.request,
                        response=error.response,
                    ) from error
                # ...or wait 1s and retry
                logger.info(f"Waiting for model to be loaded on the server: {error}")
                time.sleep(1)
                if "X-wait-for-model" not in headers and url.startswith(
                    INFERENCE_ENDPOINT
                ):
                    headers["X-wait-for-model"] = "1"
                if timeout is not None:
                    timeout = max(instance.timeout - (time.time() - t0), 1)  # type: ignore
                continue
            raise


def post_request_interceptor(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> None:
    return post(instance, *args, **kwargs)
