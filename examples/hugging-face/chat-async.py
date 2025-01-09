import asyncio

from huggingface_hub import AsyncInferenceClient

from scope3ai import Scope3AI
from scope3ai.tracers.huggingface.chat import HUGGING_FACE_CHAT_TASK


async def main():
    client = AsyncInferenceClient()
    model = client.get_recommended_model(HUGGING_FACE_CHAT_TASK)
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        response = await client.chat_completion(
            model=model,
            messages=[{"role": "user", "content": "Hello World!"}],
            max_tokens=15,
        )
        print(response)
        impact = tracer.impact()
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    asyncio.run(main())
