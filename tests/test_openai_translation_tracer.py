import pathlib

import pytest

TEST_MP3 = pathlib.Path(__file__).parent / "data" / "hello_there.mp3"


@pytest.mark.vcr
@pytest.mark.parametrize(
    "response_format", ["json", "text", "srt", "verbose_json", "vtt"]
)
@pytest.mark.parametrize("model", ["whisper-1"])
def test_openai_translation_wrapper(tracer_init, response_format, model):
    from openai import OpenAI

    client = OpenAI()
    path = TEST_MP3
    response = client.audio.translations.create(
        model=model, file=path, response_format=response_format
    )

    assert response is not None
    assert response.scope3ai is not None
    assert response.scope3ai.request.output_tokens > 0
    assert response.scope3ai.request.request_duration_ms > 0


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_format", ["json", "text", "srt", "verbose_json", "vtt"]
)
@pytest.mark.parametrize("model", ["whisper-1"])
async def test_openai_translation_wrapper_async(tracer_init, response_format, model):
    from openai import AsyncOpenAI

    client = AsyncOpenAI()
    path = TEST_MP3
    response = await client.audio.translations.create(
        model=model, file=path, response_format=response_format
    )

    assert response is not None
    assert response.scope3ai is not None
    assert response.scope3ai.request.output_tokens > 0
    assert response.scope3ai.request.request_duration_ms > 0


@pytest.mark.vcr
@pytest.mark.parametrize(
    "pathtype",
    [
        "path",
        "bytesio",
        "tuple_filename_path",
        "tuple_filename_path_contenttype",
        "tuple_filename_path_contenttype_headers",
    ],
)
@pytest.mark.parametrize("model", ["whisper-1"])
def test_openai_translation_wrapper_file_duration(tracer_init, model, pathtype):
    from openai import OpenAI

    client = OpenAI()

    if pathtype == "path":
        path = TEST_MP3
    elif pathtype == "bytesio":
        path = TEST_MP3.open(mode="rb")
    elif pathtype == "tuple_filename_path":
        path = (TEST_MP3.name, TEST_MP3.open(mode="rb"))
    elif pathtype == "tuple_filename_path_contenttype":
        path = (TEST_MP3.name, TEST_MP3.open(mode="rb"), "audio/mpeg")
    elif pathtype == "tuple_filename_path_contenttype_headers":
        path = (TEST_MP3.name, TEST_MP3.open(mode="rb"), "audio/mpeg", {})
    else:
        assert 0
        return

    response = client.audio.translations.create(
        model=model,
        file=path,
        response_format="text",
    )

    assert response is not None
    assert response.scope3ai is not None
    assert response.scope3ai.request.output_tokens > 0
    assert response.scope3ai.request.request_duration_ms > 0
    assert response.scope3ai.request.input_audio_seconds > 0
