import asyncio
from scope3ai import Scope3AI
from anthropic import Anthropic


async def main():
    client = Anthropic()
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        response = await client.chat.completions.acreate(
            model="claude-v1",
            messages=[{"role": "user", "content": "Hello!"}],
            stream=False,
        )
        print(response.choices[0].message["content"].strip())

        impact = tracer.impact()
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    asyncio.run(main())
