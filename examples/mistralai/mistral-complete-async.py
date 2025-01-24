import asyncio
from scope3ai import Scope3AI
from mistralai import Mistral

DESCRIPTION = "Mistral AI Async Completion with Environmental Impact Tracking"

ARGUMENTS = [
    {
        "name_or_flags": "--model",
        "type": str,
        "default": "mistral-large-latest",
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
        "name_or_flags": "--temperature",
        "type": float,
        "default": 0.7,
        "help": "Temperature for response generation",
    },
    {
        "name_or_flags": "--api-key",
        "type": str,
        "help": "Mistral API key (optional if set in environment)",
        "default": None,
    },
]


async def main(
    model: str,
    message: str,
    max_tokens: int,
    temperature: float,
    api_key: str | None = None,
):
    scope3 = Scope3AI.init()
    client = Mistral(api_key=api_key) if api_key else Mistral()

    with scope3.trace() as tracer:
        response = await client.chat.complete_async(
            model=model,
            messages=[{"role": "user", "content": message}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        print(response.choices[0].message.content)

        impact = tracer.impact()
        print(impact)
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
