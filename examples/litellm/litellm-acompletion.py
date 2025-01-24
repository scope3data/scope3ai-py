import asyncio
from scope3ai import Scope3AI
from litellm import acompletion

DESCRIPTION = "LiteLLM Async Completion with Environmental Impact Tracking"

ARGUMENTS = [
    {
        "name_or_flags": "--model",
        "type": str,
        "default": "claude-3-sonnet-20240229",
        "help": "Model to use for completion",
    },
    {
        "name_or_flags": "--message",
        "type": str,
        "default": "Hello!",
        "help": "Message to send to the model",
    },
    {
        "name_or_flags": "--max-tokens",
        "type": int,
        "default": 100,
        "help": "Maximum number of tokens in the response",
    },
    {
        "name_or_flags": "--api-key",
        "type": str,
        "help": "API key (optional if set in environment)",
        "default": None,
    },
]


async def main(model: str, message: str, max_tokens: int, api_key: str | None = None):
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        response = await acompletion(
            model=model,
            messages=[{"role": "user", "content": message}],
            max_tokens=max_tokens,
            api_key=api_key,
        )
        print(response.choices[0].message.content)

        impact = tracer.impact()
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="LiteLLM Completion with Environmental Impact Tracking"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="claude-3-sonnet-20240229",
        help="Model to use for completion",
    )
    parser.add_argument(
        "--message", type=str, default="Hello!", help="Message to send to the model"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=100,
        help="Maximum number of tokens in the response",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="API key (optional if set in environment)",
        default=None,
    )
    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
