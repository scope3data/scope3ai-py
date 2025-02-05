import asyncio
import os
from mistralai import Mistral

from scope3ai import Scope3AI


async def main(
    model: str,
    message: str,
    max_tokens: int,
    temperature: float,
    api_key: str | None = None,
):
    api_key = api_key or os.environ["MISTRAL_API_KEY"]
    scope3 = Scope3AI.init()
    client = Mistral(api_key=api_key) if api_key else Mistral()

    with scope3.trace() as tracer:
        chunk_count = 0
        async for chunk in await client.chat.stream_async(
            model=model,
            messages=[{"role": "user", "content": message}],
            max_tokens=max_tokens,
            temperature=temperature,
        ):
            chunk_count += 1
            print(chunk.data.choices[0].delta.content, end="", flush=True)
        print()
        print(f"Chunk count: {chunk_count}")
        impact = tracer.impact()
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Mistral AI Completion with Environmental Impact Tracking"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="mistral-large-latest",
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
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature for response generation",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Mistral API key (optional if set in environment)",
        default=None,
    )
    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
