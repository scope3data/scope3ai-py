import asyncio

from openai import AsyncOpenAI
from scope3ai import Scope3AI


async def main(text: str, model: str, response_format: str):
    client = AsyncOpenAI()
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        response = await client.audio.speech.create(
            model=model,
            voice="alloy",
            input=text,
            response_format=response_format,
        )
        print(response)
        impact = tracer.impact()
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OpenAI Speech to Text")
    parser.add_argument("--model", type=str, default="whisper-1", help="Model")
    parser.add_argument(
        "--response-format", type=str, default="json", help="Response format"
    )
    parser.add_argument("--text", type=str, help="The text to convert to speech")
    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
