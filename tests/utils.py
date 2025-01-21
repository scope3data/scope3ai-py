import base64
from pathlib import Path

TEST_IMAGE_PNG = Path(__file__).parent / "data" / "image_1024.png"
TEST_IMAGE_JPG = Path(__file__).parent / "data" / "image_512.jpg"
TEST_AUDIO_MP3 = Path(__file__).parent / "data" / "hello_there.mp3"
TEST_AUDIO_WAV = Path(__file__).parent / "data" / "hello_there.wav"


def file_as_b64str(path: Path) -> str:
    data = path.read_bytes()
    return base64.b64encode(data).decode("utf-8")


def load_image_b64(path: Path) -> str:
    media_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }
    b64 = file_as_b64str(path)
    media_type = media_types[path.suffix]
    return f"data:{media_type};base64,{b64}"
