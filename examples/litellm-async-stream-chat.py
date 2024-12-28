import asyncio
import litellm

from scope3ai import Scope3AI


async def main():
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        stream = await litellm.acompletion(
            messages=[{"role": "user", "content": "Hello World!"}],
            model="claude-3-5-sonnet-20240620",
            stream=True,
        )
        async for event in stream:
            print(event)

        impact = await tracer.aimpact()
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    asyncio.run(main())
