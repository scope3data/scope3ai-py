# Quick Start

The Scope3AI Python SDK helps you track, record and analyze the environmental
impact of your AI model usage. It provides an easy-to-use interface to the
Scope3AI API, which calculates metrics like energy consumption, CO2 emissions,
and water usage for AI model inferences.

The SDK automatically instruments popular AI libraries and platforms (OpenAI,
Anthropic, Cohere, etc.) to capture metadata about model usage. This allows you
to:

- Track impact metrics across your AI applications
- Analyze sustainability data by project, client, or environment
- Get real-time feedback on resource consumption

## Installation

Install the Scope3AI Python SDK with pip:

```bash
pip install scope3ai
```

Or with uv:

```bash
uv add scope3ai
```

## Initialize the SDK

Configure your credentials either in code or through environment variables:

```python
from scope3ai import Scope3AI

# Initialize with API key
scope3 = Scope3AI.init(
    api_key="YOUR_API_KEY",
    environment="production",
    application_id="my-app"
)
```

Or using environment variables:

```bash
export SCOPE3AI_API_KEY=YOUR_API_KEY
export SCOPE3AI_ENVIRONMENT=production
export SCOPE3AI_APPLICATION_ID=my-app
```

```python
from scope3ai import Scope3AI

scope3 = Scope3AI.init()
```

## Enable Specific Providers

By default, all supported providers are enabled if found in available installed
libraries. You can specify which ones to enable:

```python
scope3 = Scope3AI.init(
    api_key="YOUR_API_KEY",
    providers=["openai", "anthropic", "cohere"]
)
```

## Using Tracers

Use the context manager to trace API calls and get their impact:

```python
with scope3.trace() as tracer:
    # Make your API calls here
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}]
    )

    # Get impact metrics for all calls in this trace
    impact = tracer.impact()
    print(f"Total Energy: {impact.total_energy_wh} Wh")
    print(f"Total CO2: {impact.total_gco2e} gCO2e")
    print(f"Total Water: {impact.total_mlh2o} mL")
```

You can also configure metadata per-trace:

```python
with scope3.trace(
    client_id="my-client",
    project_id="my-project",
    session_id="user-123"
) as tracer:
    # Make API calls...
```

## Getting Impact Data Synchronously

Enable sync mode to get impact data immediately:

```python
scope3.sync_mode = True

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)

impact = response.scope3ai.impact
print(f"Energy used: {impact.total_energy_wh} Wh")
```
