# Scope3AI Python SDK

![PyPI - Version](https://img.shields.io/pypi/v/scope3ai)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/scope3ai)
[![Pytests](https://github.com/scope3data/scope3ai-py/actions/workflows/pytests.yml/badge.svg?branch=main&event=push)](https://github.com/scope3data/scope3ai-py/actions/workflows/pytests.yml)
[![Coverage Status](https://coveralls.io/repos/github/scope3data/scope3ai-py/badge.svg)](https://coveralls.io/github/scope3data/scope3ai-py)

Track the environmental impact of your use of AI !
The **Scope3AI Python SDK** provides an easy-to-use interface for interacting with Scope3AI's API. This library enables users to record, trace, and analyze the impact of interactions with a focus on sustainability metrics. Below are the different ways to use the SDK.

## Installation

To install the SDK, use pip:

```bash
pip install scope3ai
```

## Library and SDK support Matrix

| Library/SDK | Text generation | TTS | STT | Image Generation | Translation |
|-------------|-----------------|----|-----|------------------|-----------|
| Anthropic   | ✅              |    |     |                  |           |
| Cohere      | ✅              |     |     |                  |             |
| OpenAI      | ✅              |    |     |                  |           |
| Huggingface | ✅              | ✅  | ✅   | ✅                | ✅        |
| LiteLLM     | ✅              |    |     |                  |          |

Roadmap:
- Google
- Langchain

## Getting Started

### Initializing the SDK

The SDK can be initialized with your API key and custom configurations.

```python
from scope3ai import Scope3AI

scope3 = Scope3AI.init(
    api_key="YOUR_API_KEY",  # Replace "YOUR_API_KEY" with your actual key
    api_url="https://api.scope3.ai/v1",  # Optional: Specify the API URL
    enable_debug_logging=False,  # Enable debug logging (default: False)
    sync_mode=False,  # Enable synchronous mode when sending telemetry to the API (default: False)
)
```

### Environment variables

You can also use environment variable to setup the SDK:

- `SCOPE3AI_API_KEY`: Your Scope3AI API key
- `SCOPE3AI_API_URL`: The API endpoint URL. Default: `https://api.scope3.ai/v1`
- `SCOPE3AI_SYNC_MODE`: If `True`, every interaction will be send synchronously to the API, otherwise it will use a background worker. Default: `False`

```python
from scope3ai import Scope3AI

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

## Development

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

```bash
$ uv run datamodel-codegen \
    --input tests/api-mocks/aiapi.yaml \
    --input-file-type openapi \
    --output scope3ai/api/typesgen.py \
    --output-model-type pydantic_v2.BaseModel \
    --use-schema-description \
    --allow-extra-fields \
    && uv run ruff format scope3ai/api/typesgen.py
```
