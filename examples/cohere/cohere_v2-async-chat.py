import asyncio
import cohere
from scope3ai import Scope3AI

DESCRIPTION = "Cohere v2 Async Chat Completion with Environmental Impact Tracking"

ARGUMENTS = [
    {
        "name_or_flags": "--model",
        "type": str,
        "default": "command-r-plus-08-2024",
        "help": "Model to use for chat completion",
    },
    {
        "name_or_flags": "--message",
        "type": str,
        "default": "Hello world!",
        "help": "Message to send to the chat model",
    },
    {
        "name_or_flags": "--role",
        "type": str,
        "default": "user",
        "help": "Role for the message",
    },
    {
        "name_or_flags": "--api-key",
        "type": str,
        "help": "Cohere API key (optional if set in environment)",
        "default": None,
    },
]


async def main(model: str, message: str, role: str, api_key: str | None = None):
    scope3 = Scope3AI.init()
    co = cohere.AsyncClientV2(api_key=api_key) if api_key else cohere.AsyncClientV2()

    with scope3.trace() as tracer:
        response = await co.chat(
            model=model,
            messages=[{"role": role, "content": message}],
        )
        print(response)

        impact = tracer.impact()
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=DESCRIPTION)
    for argument in ARGUMENTS:
        parser.add_argument(**argument)
    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
