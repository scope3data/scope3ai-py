import asyncio
from scope3ai import Scope3AI
from openai import AsyncOpenAI


async def main(model: str, prompt: str, n: int, size: str):
    client = AsyncOpenAI()
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        response = await client.images.generate(
            model=model,
            prompt=prompt,
            n=n,
            size=size,
        )
        print(response.data[0].url)

        impact = tracer.impact()
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenAI Image Generation with Environmental Impact Tracking"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="dall-e-2",
        help="Model to use for image generation",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="A beautiful landscape",
        help="Prompt for image generation",
    )
    parser.add_argument("--n", type=int, default=1, help="Number of images to generate")
    parser.add_argument(
        "--size", type=str, default="512x512", help="Size of the generated image"
    )
    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
