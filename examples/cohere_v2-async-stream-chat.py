import asyncio

import cohere

from scope3ai import Scope3AI


async def main():
    scope3 = Scope3AI.init()
    co = cohere.AsyncClientV2()

    with scope3.trace() as tracer:
        stream = co.chat_stream(
            model="command-r-plus-08-2024",
            messages=[{"role": "user", "content": "Hello world!"}],
            max_tokens=100,
        )
        async for event in stream:
            print(event)

        impact = await tracer.aimpact()
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    asyncio.run(main())
