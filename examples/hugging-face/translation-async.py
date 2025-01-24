# translation-async.py
import asyncio

from huggingface_hub import AsyncInferenceClient

from scope3ai import Scope3AI
from scope3ai.tracers.huggingface.translation import HUGGING_FACE_TRANSLATION_TASK


async def main(model: str | None, text: str, target_language: str):
    client = AsyncInferenceClient()
    scope3 = Scope3AI.init()
    model_to_use = (
        model
        if model
        else await client.get_recommended_model(HUGGING_FACE_TRANSLATION_TASK)
    )

    with scope3.trace() as tracer:
        response = await client.translation(
            model=model_to_use,
            text=text,
            target_language=target_language,
        )
        print("Translation Response:", response)
        impact = tracer.impact(response)
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Hugging Face Translation with Environmental Impact Tracking"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Model to use (default: recommended model)",
    )
    parser.add_argument(
        "--text", type=str, default="Hello, how are you?", help="Text to translate"
    )
    parser.add_argument(
        "--target-language",
        type=str,
        default="es",
        help='Target language code (e.g., "es" for Spanish)',
    )
    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
