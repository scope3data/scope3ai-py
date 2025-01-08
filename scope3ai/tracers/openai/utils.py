import logging
from typing import Optional

import openai

logger = logging.getLogger("scope3.tracers.openai")


def _get_file_audio_duration(
    file: openai._types.FileTypes,
) -> Optional[float]:
    try:
        from mutagen import File

        if isinstance(file, (list, tuple)):
            file = file[1]

        audio = File(file)
        if audio is not None and audio.info is not None:
            return audio.info.length
    except Exception as e:
        logger.exception(f"Failed to get audio duration: {e}")
    return None
