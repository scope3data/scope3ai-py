# Scope3AI Python SDK - Python SDK for Scope3 AI API

Track the environmental impact of your use of AI !
The **Scope3AI Python SDK** provides an easy-to-use interface for interacting with Scope3AI's API. This library enables users to record, trace, and analyze the impact of interactions with a focus on sustainability metrics. Below are the different ways to use the SDK.

## Installation

To install the SDK, use pip:

```bash
pip install scope3ai
```

## Getting Started

### Initializing the SDK

The SDK can be initialized with your API key and custom configurations.

```python
from scope3ai import Scope3AI

scope3 = Scope3AI.init(
    api_key="YOUR_API_KEY",  # Replace "YOUR_API_KEY" with your actual key
    api_url="https://api.scope3.ai/v1",  # Optional: Specify the API URL
    include_impact_response=False,  # Include impact in responses (default: False)
    enable_debug_logging=False,  # Enable debug logging (default: False)
)
```

### Environment variables

You can also use environment variable to setup the SDK:

- `SCOPE3AI_API_KEY`: Your Scope3AI API key
- `SCOPE3AI_API_URL`: The API endpoint URL. Default: `https://api.scope3.ai/v1`
- `SCOPE3AI_INCLUDE_IMPACT_RESPONSE`: If `True`, every interaction will include its impact in the response. Default: `False`

```python
from scope3ai import Scope3AI

scope3 = Scope3AI.init()
```

## Usage Examples

### 1. Using Context Management for Tracing

You can record interactions using a `trace()` context. This allows you to analyze the sustainability impact of all interactions within the context.

```python
with scope3.trace() as tracer:
    # Perform your interactions
    interact()

    # Print the impact of the recorded trace
    print(tracer.impact())
```

### 2. Recording `trace_id` for Later Usage

Store the `trace_id` during the interaction for querying the impact later.

```python
trace_id = None
with scope3.trace() as tracer:
    trace_id = tracer.trace_id
    interact()

# Fetch and print the impact using the stored trace_id
print(scope3.impact(trace_id=trace_id))
```

### 3. Using `record_id` from the Interaction Response

Retrieve the `record_id` from the interaction response and query the impact.

```python
response = interact()
print(scope3.impact(record_id=response.scope3ai.record_id))
```

#### Alternative: Fetch Impact for Multiple Records

You can query impacts for multiple `record_id`s simultaneously:

```python
record_ids = [response.scope3ai.record_id]
print(scope3.impact_many(record_ids=record_ids))
```

### 4. Enabling Synchronous Mode for Immediate Impact Response

In synchronous mode, the SDK will include the impact data directly in the interaction response. This ensures that every interaction immediately returns its impact data.

```python
scope3.include_impact_response = True

response = interact()
print(response.scope3ai.impact)
```

### 5. Specify name for grouping

You can specify a name for grouping the interactions. This is useful for grouping interactions based on a specific context.

```python
with scope3.trace(name="my_workflow"):
    interact()
    with scope3.trace(name="image_generation"):
        generate_image()
        save_to_s3()
    interact()
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
