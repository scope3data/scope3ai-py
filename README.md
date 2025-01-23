<div align="center">
<a href="https://scope3.com"><img src="https://github.com/user-attachments/assets/b429d87f-68db-4d67-adde-1093cd80e9a7" alt="scope3 logo" width="200px"/></a>

# Scope3AI Python SDK

**Track the environmental impact of your use of AI !**

The **Scope3AI Python SDK** provides an easy-to-use interface for interacting with [Scope3AI's API](https://aidocs.scope3.com/docs/overview).<br/>
It allow you to record, trace, and analyze the impact of interactions with a focus on sustainability metrics.

![PyPI - Version](https://img.shields.io/pypi/v/scope3ai)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/scope3ai)
[![Pytests](https://github.com/scope3data/scope3ai-py/actions/workflows/pytests.yml/badge.svg?branch=main&event=push)](https://github.com/scope3data/scope3ai-py/actions/workflows/pytests.yml)
[![Coverage Status](https://coveralls.io/repos/github/scope3data/scope3ai-py/badge.svg)](https://coveralls.io/github/scope3data/scope3ai-py)

</div>

## 🚀 Installation

The package `scope3ai` SDK is published on [pypi](https://pypi.org/project/scope3ai/). You can install it using `pip`:
```bash
pip install scope3ai
```

We personally use [`uv`](https://github.com/astral-sh/uv):
```bash
uv add scope3ai
```

## 📚 Library and SDK support Matrix

| Library/SDK | Text generation | TTS | STT | Image Generation | Translation | Multimodal input | Multimodal output |
|-------------|-----------------|----|-----|------------------|-----------|------------------|-------------------|
| Anthropic   | ✅              |    |     |                  |           |                  |
| Cohere      | ✅              |    |     |                  |           |                  |
| OpenAI      | ✅              | ✅ | ✅  | ✅               | ✅        | Images/Audio     |
| Huggingface | ✅              | ✅ | ✅  | ✅               | ✅        |                  |
| LiteLLM     | ✅              |    |     |                  |           | Images/Audio     |
| MistralAi   | ✅              |    |     |                  |           | Images           |

Roadmap:
- Google
- Langchain

## ✨ Getting Started

### Initializing the SDK

The SDK can be initialized with the following parameters, from environemnt variable or when calling `ScopeAI.init(...)`:

| Attribute             | Environment Variable     | Description    | Can be customized per tracer |
|-----------------------|--------------------------|--------------------------------|------------------------------|
| **`api_key`**         | **`SCOPE3AI_API_KEY`**   | Your Scope3AI API key. Default: `None` | **No**                       |
| `api_url`             | `SCOPE3AI_API_URL`       | The API endpoint URL. Default: `https://aiapi.scope3.com` | No                           |
| `enable_debug_logging`| `SCOPE3AI_DEBUG_LOGGING` | Enable debug logging. Default: `False` | No                           |
| `sync_mode`           | `SCOPE3AI_SYNC_MODE`     | Enable synchronous mode. Default: `False` | No                           |
| `environment`         | `SCOPE3AI_ENVIRONMENT`   | The user-defined environment name, such as "production" or "staging". Default: `None` | No                           |
| `application_id`      | `SCOPE3AI_APPLICATION_ID`| The user-defined application identifier. Default: `default` | ✅ Yes                       |
| `client_id`           | `SCOPE3AI_CLIENT_ID`     | The user-defined client identifier. Default: `None` | ✅ Yes                       |
| `project_id`          | `SCOPE3AI_PROJECT_ID`    | The user-defined project identifier. Default: `None` | ✅ Yes                       |
| `session_id`          | -                        | The user-defined session identifier, used to track user session. Default `None`. Available only at tracer() level. | ✅ Yes                       |


**Here is an example of how to initialize the SDK**:

```python
from scope3ai import Scope3AI

scope3 = Scope3AI.init(
    api_key="YOUR_API_KEY",
    environment="staging",
    application_id="my-app",
    project_id="my-webinar-2024"
)
```

**You could also use environment variables to initialize the SDK**:

1. Create a `.env` file with the following content:

```env
SCOPE3AI_API_KEY=YOUR_API_KEY
SCOPE3AI_ENVIRONMENT=staging
SCOPE3AI_APPLICATION_ID=my-app
SCOPE3AI_PROJECT_ID=my-webinar-2024
```

2. Use dotenv to load the environment variables:

```python
from dotenv import load_dotenv
from scope3ai import Scope3AI

load_dotenv()
scope3 = Scope3AI.init()
```

## Usage Examples

### 1. Using Context Management for Tracing

Within the context of a `trace`, all interactions are recorded and you can query the impact of the trace.
As the interactions are captured and send to Scope3 AI for analysis, the impact is calculated and returned asynchronously.
This will automatically wait for all traces to be processed and return the impact.

```python
with scope3.trace() as tracer:
    # Perform your interactions
    interact()
    interact()

    # Print the impact of the recorded trace
    impact = tracer.impact()
    print(f"Total Energy Wh: {impact.total_energy_wh}")
    print(f"Total GCO2e: {impact.total_gco2e}")
    print(f"Total MLH2O: {impact.total_mlh2o}")
```

### 2. Configure per-tracer metadata

Some global metadata can be overridden per-tracer. This is useful when you want to mark a specific tracer with a different `client_id` or `project_id`.

```python
with scope3.trace(client_id="my-client", project_id="my-project") as tracer:
    ...
```

You can track session with the `session_id` parameter of the tracer. This is only for categorizing the traces in the dashboard.
but works at tracer level, not in global level like `client_id` or `project_id` or others.

```python
with scope3.trace(session_id="my-session") as tracer:
    ...
```

### 2. Single interaction

For a single interaction, the response is augmented with a `scope3ai` attribute that contains the
`request` and `impact` data. The impact data is calculated asynchronously so we need to wait
for the impact to be calculated and for the attribute to be ready.

```python
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello world"}],
    stream=False,
)

response.scope3ai.wait_impact()
impact = response.scope3ai.impact
print(f"Total Energy Wh: {impact.total_energy_wh}")
print(f"Total GCO2e: {impact.total_gco2e}")
print(f"Total MLH2O: {impact.total_mlh2o}")
```

### 3. Enabling Synchronous Mode for Immediate Impact Response

In synchronous mode, the SDK will include the impact data directly in the interaction response.
This is useful when you want to get the impact data immediately after the interaction without waiting.

```python
scope3.sync_mode = True

response = interact()
impact = response.scope3ai.impact
print(f"Total Energy Wh: {impact.total_energy_wh}")
print(f"Total GCO2e: {impact.total_gco2e}")
print(f"Total MLH2O: {impact.total_mlh2o}")
```

## 🛠️ Development

This project use conventional commits and semantic versioning.

Also:
- [pre-commit](https://pre-commit.com) for code formatting, linting and conventional commit checks
- [uv](https://github.com/astral-sh/uv) for project and dependency management.

### Initial setup

```bash
$ pre-commit install
$ pre-commit install --hook-type commit-msg
```

## Using with specific env

You can use `UV_ENV_FILE` or `--env-file` to specify the environment file to use.

```bash
$ export UV_ENV_FILE=.env
$ uv sync --all-extras --all-groups
$ uv run python -m examples.openai-sync-chat
```

## Update typesgen.py

The `typesgen.py` script is derivated from the `aiapi.yaml`.
This script will download the latest YAML file, patch it if necessary
and generate the `typesgen.py` file.

```bash
$ uv run tools/sync-api.py
```
