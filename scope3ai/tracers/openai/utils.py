import importlib
import io
import logging
from typing import Optional

import openai

logger = logging.getLogger("scope3.tracers.openai")


def _lazy_import(module_name: str, class_name: str):
    def _imported():
        module = importlib.import_module(module_name)
        return getattr(module, class_name)

    return _imported


MUTAGEN_MAPPING = {
    "mp3": _lazy_import("mutagen.mp3", "MP3"),
    "aac": _lazy_import("mutagen.aac", "AAC"),
    "opus": _lazy_import("mutagen.oggopus", "OggOpus"),
    "flac": _lazy_import("mutagen.flac", "FLAC"),
    "wav": _lazy_import("mutagen.wave", "WAVE"),
}


def _get_audio_duration(format: str, content: bytes) -> Optional[float]:
    try:
        mutagen_cls = MUTAGEN_MAPPING.get(format)
        if mutagen_cls is None:
            logger.error(f"Unsupported audio format: {format}")
            return None
        else:
            mutagen_file = mutagen_cls()(io.BytesIO(content))
            duration = mutagen_file.info.length
    except Exception:
        logger.exception("Failed to estimate audio duration")
        return None

    if format == "wav":
        # bug in mutagen, it returns high number for wav files
        duration = len(content) * 8 / mutagen_file.info.bitrate

    return duration


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
