import asyncio
from scope3ai import Scope3AI
from openai import AsyncOpenAI


async def main():
    client = AsyncOpenAI()
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello!"}],
            stream=True,
        )
        async for event in response:
            if not event.choices:
                continue
            print(event.choices[0].delta.content, end="", flush=True)
        print()

        impact = tracer.impact()
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    asyncio.run(main())
