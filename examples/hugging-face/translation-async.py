import asyncio

from huggingface_hub import AsyncInferenceClient

from scope3ai import Scope3AI
from scope3ai.tracers.huggingface.translation import HUGGING_FACE_TRANSLATION_TASK


async def main():
    client = AsyncInferenceClient()
    scope3 = Scope3AI.init()
    model = await client.get_recommended_model(HUGGING_FACE_TRANSLATION_TASK)

    with scope3.trace() as tracer:
        response = await client.translation(
            model=model,
            text="Hello, how are you?",
            target_language="es",  # Spanish
        )
        print("Translation Response:", response)
        impact = tracer.impact(response)
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    asyncio.run(main())
