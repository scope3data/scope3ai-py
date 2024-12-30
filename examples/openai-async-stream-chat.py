import asyncio
from scope3ai import Scope3AI
from openai import OpenAI

async def main():
    client = OpenAI()
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        response = await client.chat.completions.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello!"}],
            stream=True
        )
        async for event in response:
            print(event.choices[0].delta['content'].strip())

        impact = tracer.impact()
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")

if __name__ == "__main__":
    asyncio.run(main())
