from enum import Enum
from typing import Optional


# client is an API provided by managed service providers or third parties to interact with managed service providers
class CLIENTS(Enum):
    # some clients hide more than 1 provider, like monsieur Google. We want to distinguish between attaching to a client and sending a provider
    GOOGLE_GENAI = "google-genai"

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    HUGGINGFACE_HUB = "huggingface"
    LITELLM = "litellm"  # WARN - special
    MISTRALAI = "mistral"
    RESPONSE = "response"
    # TODO - this is full list
    # AWS_BEDROCK = "aws-bedrock"
    # AZURE_OPENAI = "azure-openai"
    # IBM_WATSONX = "ibm-watsonx"
    # ORACLE_AI = "oracle-ai"
    # ALIBABA_PAI = "alibaba-pai"
    # TENCENT_HUNYUAN = "tencent-hunyuan"
    # YANDEX_YAGPT = "yandex-yagpt"
    # REPLICATE = "replicate"
    # AI21 = "ai21"
    # TOGETHER = "together"
    # ANYSCALE = "anyscale"
    # DEEPINFRA = "deepinfra"
    # PERPLEXITY = "perplexity"
    # GROQ = "groq"
    # FIREWORKS = "fireworks"
    # FOREFRONT = "forefront"
    # NVIDIA_NEMO = "nvidia-nemo"
    # STABILITY_AI = "stability-ai"
    # META_LLAMA = "meta-llama"
    # INFLECTION_AI = "inflection-ai"
    # DATABRICKS = "databricks"
    # WRITER = "writer"


# codependency ref 2E92DAFC-3800-4E36-899B-18E842ADB8E3 https://github.com/scope3data/aiapi
# TODO get from openapi
# providers are APIs provided by managed service providers; since having multiple APIs for one managed service provider is rare (oh hi Google), we just keep calling it all "managed service providers"
class PROVIDERS(Enum):
    GOOGLE_GEMINI = "google-gemini"
    GOOGLE_VERTEX = "google-vertex"

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    HUGGINGFACE_HUB = "huggingface"
    LITELLM = "litellm"  # WARN - special
    MISTRALAI = "mistral"
    RESPONSE = "response"


# API to Provider are many to many
# but we assume they x = x for all the providers/clients in PROVIDER_CLIENTS
PROVIDER_TO_CLIENT = {
    PROVIDERS.GOOGLE_GEMINI: [CLIENTS.GOOGLE_GENAI],
    PROVIDERS.GOOGLE_VERTEX: [CLIENTS.GOOGLE_GENAI],
    PROVIDERS.OPENAI: [CLIENTS.OPENAI],
    PROVIDERS.ANTHROPIC: [CLIENTS.ANTHROPIC],
    PROVIDERS.COHERE: [CLIENTS.COHERE],
    PROVIDERS.HUGGINGFACE_HUB: [CLIENTS.HUGGINGFACE_HUB],
    PROVIDERS.LITELLM: [CLIENTS.LITELLM],
    PROVIDERS.MISTRALAI: [CLIENTS.MISTRALAI],
    PROVIDERS.RESPONSE: [CLIENTS.RESPONSE],
}

CLIENT_TO_PROVIDER = {}
for k, v in PROVIDER_TO_CLIENT.items():
    for client in v:
        if client not in CLIENT_TO_PROVIDER:
            CLIENT_TO_PROVIDER[client] = []
        CLIENT_TO_PROVIDER[client].append(k)


def try_provider_for_client(client: CLIENTS) -> Optional[PROVIDERS]:
    r = CLIENT_TO_PROVIDER.get(client)
    if r is None:
        # client without provider is a coding error. throw, crash everything
        raise ValueError(f"client {client} has no provider")
    # not determined or emptiness
    if len(r) > 1 or len(r) == 0:
        return None
    return r[0]
