# Configuration

The SDK can be configured either through environment variables or when calling `Scope3AI.init()`.

The following environment variables are supported:

| Environment Variable | Description | Scope3AI.init | Tracer |
|---------------------|-------------|---------------|--------------|
| `SCOPE3AI_API_KEY` | Required. Your Scope3AI API key | [api_key](/scope3ai/#scope3ai.lib.Scope3AI.init) | |
| `SCOPE3AI_API_URL` | The API endpoint URL | [api_url](/scope3ai/#scope3ai.lib.Scope3AI.init) | |
| `SCOPE3AI_DEBUG_LOGGING` | Enable debug logging | [enable_debug_logging](/scope3ai/#scope3ai.lib.Scope3AI.init) | |
| `SCOPE3AI_SYNC_MODE` | Enable synchronous mode | [sync_mode](/scope3ai/#scope3ai.lib.Scope3AI.init) | |
| `SCOPE3AI_ENVIRONMENT` | User-defined environment name (e.g. "production", "staging") | [environment](/scope3ai/#scope3ai.lib.Scope3AI.init) | |
| `SCOPE3AI_APPLICATION_ID` | User-defined application identifier | [application_id](/scope3ai/#scope3ai.lib.Scope3AI.init) | [application_id](/tracer/#scope3ai.api.tracer.Tracer) |
| `SCOPE3AI_CLIENT_ID` | User-defined client identifier | [client_id](/scope3ai/#scope3ai.lib.Scope3AI.init) | [client_id](/tracer/#scope3ai.api.tracer.Tracer) |
| `SCOPE3AI_PROJECT_ID` | User-defined project identifier | [project_id](/scope3ai/#scope3ai.lib.Scope3AI.init) | [project_id](/tracer/#scope3ai.api.tracer.Tracer) |

Example using environment variables:

```env
SCOPE3AI_API_KEY=your_api_key_here
SCOPE3AI_ENVIRONMENT=staging
SCOPE3AI_APPLICATION_ID=my-app
SCOPE3AI_PROJECT_ID=my-project
```

Example using initialization parameters in `Scope3AI.init()`:

```python
scope3 = Scope3AI.init(
    api_key="your_api_key_here",
    environment="staging",
    application_id="my-app",
    project_id="my-project",
    sync_mode=True,
    enable_debug_logging=True
)
```

Example using initialization parameters in `Tracer`:

```python
scope3 = Scope3AI.init(
    api_key="your_api_key_here",
)

# Override application ID for this specific trace
with scope3.trace(application_id="my-specific-app") as tracer:
    # Run operations with "my-specific-app" identifier
    interact()
```
