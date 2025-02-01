# Using Tracer

Tracers are the core feature of the Scope3AI SDK that allow you to track the
environmental impact of your AI model usage. Here's a detailed guide on using
tracers effectively:

## Basic Tracing

The most basic way to use tracers is with a context manager:

```python
from scope3ai import Scope3AI

scope3 = Scope3AI.init(api_key="YOUR_API_KEY")

with scope3.trace() as tracer:
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )

    # Get impact metrics
    impact = tracer.impact()
    print(f"Energy: {impact.total_energy_wh} Wh")
    print(f"CO2: {impact.total_gco2e} gCO2e")
    print(f"Water: {impact.total_mlh2o} mL")
```

## Nested Traces

You can nest traces to track different parts of your application:

```python
with scope3.trace(project_id="outer-project") as outer:
    # First API call
    response1 = openai.chat.completions.create(...)

    with scope3.trace(project_id="inner-project") as inner:
        # Second API call
        response2 = openai.chat.completions.create(...)

        # Get impact for inner trace only
        inner_impact = inner.impact()

    # Get impact for all calls
    total_impact = outer.impact()
```

## Per-Trace Metadata

Each trace can have its own metadata:

```python
with scope3.trace(
    client_id="client-123",
    project_id="summarization-project",
    application_id="doc-processor",
    session_id="user-session-456"
) as tracer:
    # API calls will be tagged with this metadata
    response = openai.chat.completions.create(...)
```

## Async Usage

The tracer works with async code:

```python
async def process():
    with scope3.trace() as tracer:
        response = await openai.chat.completions.create(...)
        await response.scope3ai.wait_impact()
        impact = response.scope3ai.impact
```

## Direct Impact Access

Each response object is augmented with a scope3ai attribute:

```python
response = openai.chat.completions.create(...)

# Wait for impact calculation if in async mode
response.scope3ai.wait_impact()

# Access impact metrics
impact = response.scope3ai.impact
print(f"Energy: {impact.total_energy_wh} Wh")
```

## Synchronous Mode

Enable sync mode to get impact data immediately:

```python
scope3.sync_mode = True

with scope3.trace() as tracer:
    response = openai.chat.completions.create(...)
    # Impact is immediately available
    print(response.scope3ai.impact.total_energy_wh)
```

## Trace Impact Types

The impact() method returns an object with these metrics:

- total_energy_wh: Energy usage in watt-hours
- total_gco2e: CO2 emissions in grams of CO2 equivalent
- total_mlh2o: Water usage in milliliters

Each also includes detailed breakdowns for:
- inference_impact: Impact from model inference
- training_impact: Impact from model training
- total_impact: Combined total impact

## Error Handling

Tracers handle errors gracefully:

```python
with scope3.trace() as tracer:
    try:
        response = openai.chat.completions.create(...)
    except Exception as e:
        # Impact is still calculated for any successful calls
        impact = tracer.impact()
```
