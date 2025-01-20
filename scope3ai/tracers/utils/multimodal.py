import base64
import logging
from io import BytesIO

from scope3ai.api.types import ImpactRow
from scope3ai.api.typesgen import Image as RootImage
from scope3ai.tracers.utils.audio import MUTAGEN_MAPPING, _get_audio_duration


def aggregate_multimodal_image(content: dict, row: ImpactRow) -> None:
    from PIL import Image

    url = content["image_url"]["url"]
    if url.startswith("data:"):
        # extract content type, and data part
        # example: data:image/jpeg;base64,....
        content_type, data = url.split(",", 1)
        image_data = BytesIO(base64.b64decode(data))
        image = Image.open(image_data)
        width, height = image.size
        size = RootImage(root=f"{width}x{height}")

        if row.input_images is None:
            row.input_images = [size]
        else:
            row.input_images.append(size)

    else:
        # TODO: not supported yet.
        # Should we actually download the file here just to have the size ??
        pass


def aggregate_multimodal_audio(content: dict, row: ImpactRow) -> None:
    input_audio = content["input_audio"]
    format = input_audio["format"]
    b64data = input_audio["data"]
    assert format in MUTAGEN_MAPPING

    # decode the base64 data
    audio_data = base64.b64decode(b64data)
    # TODO: accept audio duration as float in AiApi
    duration = int(_get_audio_duration(format, audio_data))

    if row.input_audio_seconds is None:
        row.input_audio_seconds = duration
    else:
        row.input_audio_seconds += duration


def aggregate_multimodal_content(
    content: dict, row: ImpactRow, logger: logging.Logger
) -> None:
    try:
        content_type = content.get("type")
        if content_type == "image_url":
            aggregate_multimodal_image(content, row)
        elif content_type == "input_audio":
            aggregate_multimodal_audio(content, row)
    except Exception as e:
        logger.error(f"Error processing multimodal content: {e}")


def aggregate_multimodal(message: dict, row: ImpactRow, logger: logging.Logger) -> None:
    # if the message content is not a tuple/list, it's just text.
    # so there is nothing multimodal in it, we can just forget about it.
    content = message.get("content", [])
    if isinstance(content, (tuple, list)):
        for item in content:
            aggregate_multimodal_content(item, row, logger)
