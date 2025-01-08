from enum import Enum


class PROVIDERS(Enum):
    ANTROPIC = "anthropic"
    COHERE = "cohere"
    OPENAI = "openai"
    HUGGINGFACE_HUB = "huggingface_hub"
    LITELLM = "litellm"
    MISTRALAI = "mistralai"
    RESPONSE = "response"
