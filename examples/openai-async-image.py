import asyncio
from scope3ai import Scope3AI
from openai import AsyncOpenAI


async def main():
    client = AsyncOpenAI()
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        response = await client.images.generate(
            model="dall-e-2",
            prompt="A beautiful landscape",
            n=1,
            size="512x512",
        )
        print(response.data[0].url)

        impact = tracer.impact()
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    asyncio.run(main())
