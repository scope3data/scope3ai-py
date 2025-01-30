import pytest
from google import genai
import os


@pytest.mark.vcr
def test_gemini_chat(tracer_with_sync_init):
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp", contents="How does RLHF work?"
    )
    print(response.text)
    # GenerateContentResponse


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_gemini_chat_async(tracer_with_sync_init):
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    response = await client.aio.models.generate_content(
        model="gemini-2.0-flash-exp", contents="How does RLHF work?"
    )
    print(response.text)
    # GenerateContentResponse


@pytest.mark.vcr
def test_gemini_chat_stream(tracer_with_sync_init):
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    chat = client.chats.create(model="gemini-2.0-flash-exp")
    for chunk in chat.send_message_stream("tell me a story"):
        # GenerateContentResponse
        print(chunk.text, end="")


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_gemini_chat_stream_async(tracer_with_sync_init):
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    chat = client.aio.chats.create(model="gemini-2.0-flash-exp")
    async for chunk in await chat.send_message_stream("tell me a story"):
        # GenerateContentResponse
        print(chunk.text, end="")


# @pytest.mark.vcr
# def test_gemini_text_to_image(tracer_with_sync_init):
#     client = genai.Client(api_key='GEMINI_API_KEY')
#     response = client.models.generate_images(model='imagen-3.0-generate-002', prompt='Fuzzy bunnies in my kitchen',
#     config=types.GenerateImagesConfig(
#         negative_prompt= 'people',
#         number_of_images= 1,
#         include_rai_reason= True,
#         output_mime_type= 'image/jpeg'
#     ))
#     print(response)

# @pytest.mark.vcr
# @pytest.mark.asyncio
# async def test_gemini_async_chat(tracer_with_sync_init):
#     model = genai.GenerativeModel(api_key='GEMINI_API_KEY', model='gemini-1.5-flash')
#     response = await model.generate_content_async(contents='How does RLHF work?')
#     print(response.text)

# @pytest.mark.vcr
# def test_gemini_stream_chat(tracer_with_sync_init):
#     client =  genai.Client(api_key='GEMINI_API_KEY')


# @pytest.mark.vcr
# @pytest.mark.asyncio
# async def test_gemini_async_stream_chat(tracer_with_sync_init):
#     client =  genai.Client(api_key='GEMINI_API_KEY')
