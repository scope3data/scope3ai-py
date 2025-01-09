import asyncio
from scope3ai import Scope3AI
from anthropic import AsyncAnthropic


async def main():
    client = AsyncAnthropic()
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        response = await client.messages.create(
            model="claude-3-5-sonnet-latest",
            messages=[{"role": "user", "content": "Hello!"}],
            max_tokens=100,
        )
        print(response.content[0].text.strip())

        impact = tracer.impact()
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    asyncio.run(main())
