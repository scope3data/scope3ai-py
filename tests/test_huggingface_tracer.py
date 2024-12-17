import pytest
from huggingface_hub import InferenceClient


@pytest.mark.vcr
def test_huggingface_chat(tracer_init):
    client = InferenceClient()
    output = client.chat.completions.create(
        messages=[{"role": "user", "content": {"type": "text", "text": "Hello World!"}}]
    )
    print(output)
