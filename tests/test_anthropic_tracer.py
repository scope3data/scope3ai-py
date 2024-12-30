import pytest
from anthropic import Anthropic, AsyncAnthropic


@pytest.mark.vcr
def test_anthropic_chat(tracer_init):
    client = Anthropic()
    response = client.messages.create(
        max_tokens=100,
        messages=[{"role": "user", "content": "Hello World!"}],
        model="claude-3-5-sonnet-20240620",
    )
    assert len(response.content) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 10
    assert response.scope3ai.request.output_tokens == 37
    assert response.scope3ai.impact is None


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_anthropic_async_chat(tracer_init):
    client = AsyncAnthropic()
    response = await client.messages.create(
        max_tokens=100,
        messages=[{"role": "user", "content": "Hello World!"}],
        model="claude-3-5-sonnet-20240620",
    )
    assert len(response.content) > 0
    assert getattr(response, "scope3ai") is not None
    assert response.scope3ai.request.input_tokens == 10
    assert response.scope3ai.request.output_tokens == 43
    assert response.scope3ai.impact is None


@pytest.mark.vcr
def test_anthropic_stream_chat(tracer_init):
    client = Anthropic()

    text_response = ""
    with client.messages.stream(
        max_tokens=100,
        messages=[{"role": "user", "content": "Hello World!"}],
        model="claude-3-5-sonnet-20240620",
    ) as stream:
        for text in stream.text_stream:
            text_response += text

        assert getattr(stream, "scope3ai") is not None
        assert stream.scope3ai.request.input_tokens == 10
        assert stream.scope3ai.request.output_tokens == 45
        assert stream.scope3ai.impact is None

    assert len(text_response) > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_anthropic_async_stream_chat(tracer_init):
    client = AsyncAnthropic()

    text_response = ""
    async with client.messages.stream(
        max_tokens=100,
        messages=[{"role": "user", "content": "Hello World!"}],
        model="claude-3-5-sonnet-20240620",
    ) as stream:
        async for text in stream.text_stream:
            text_response += text

        assert getattr(stream, "scope3ai") is not None
        assert stream.scope3ai.request.input_tokens == 10
        assert stream.scope3ai.request.output_tokens == 44
        assert stream.scope3ai.impact is None

    assert len(text_response) > 0


@pytest.mark.vcr
def test_anthropic_stream_chat_from_create_context(tracer_init):
    client = Anthropic()

    with client.messages.create(
        max_tokens=100,
        messages=[{"role": "user", "content": "Hello World!"}],
        model="claude-3-5-sonnet-20240620",
        stream=True,
    ) as stream:
        assert getattr(stream, "scope3ai") is None

        for entry in stream:
            print(entry)

        assert getattr(stream, "scope3ai") is not None
        assert stream.scope3ai.request.input_tokens == 10
        assert stream.scope3ai.request.output_tokens == 31
        assert stream.scope3ai.impact is None


@pytest.mark.vcr
def test_anthropic_stream_chat_from_create_linear(tracer_init):
    client = Anthropic()

    stream = client.messages.create(
        max_tokens=100,
        messages=[{"role": "user", "content": "Hello World!"}],
        model="claude-3-5-sonnet-20240620",
        stream=True,
    )
    assert getattr(stream, "scope3ai") is None

    for entry in stream:
        print(entry)

    assert getattr(stream, "scope3ai") is not None
    assert stream.scope3ai.request.input_tokens == 10
    assert stream.scope3ai.request.output_tokens == 37
    assert stream.scope3ai.impact is None


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_anthropic_stream_async_chat_from_create_linear(tracer_init):
    client = AsyncAnthropic()

    stream = await client.messages.create(
        max_tokens=100,
        messages=[{"role": "user", "content": "Hello World!"}],
        model="claude-3-5-sonnet-20240620",
        stream=True,
    )
    assert getattr(stream, "scope3ai") is None

    async for entry in stream:
        print(entry)

    assert getattr(stream, "scope3ai") is not None
    assert stream.scope3ai.request.input_tokens == 10
    assert stream.scope3ai.request.output_tokens == 31
    assert stream.scope3ai.impact is None
