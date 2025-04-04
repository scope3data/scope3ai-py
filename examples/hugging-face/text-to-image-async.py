# text-to-image-async.py
import asyncio

from huggingface_hub import AsyncInferenceClient

from scope3ai import Scope3AI
from scope3ai.tracers.huggingface.text_to_image import HUGGING_FACE_TEXT_TO_IMAGE_TASK


async def main(model: str | None, prompt: str, num_images: int):
    client = AsyncInferenceClient()
    scope3 = Scope3AI.init()
    model_to_use = (
        model
        if model
        else client.get_recommended_model(HUGGING_FACE_TEXT_TO_IMAGE_TASK)
    )

    with scope3.trace() as tracer:
        response = await client.text_to_image(
            model=model_to_use,
            prompt=prompt,
            num_images=num_images,
        )
        print("Text to Image Response:", response)
        impact = tracer.impact(response)
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Hugging Face Text-to-Image Generation with Environmental Impact Tracking"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Model to use (default: recommended model)",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="A serene forest with sunlight filtering through trees",
        help="Text prompt for image generation",
    )
    parser.add_argument(
        "--num-images", type=int, default=1, help="Number of images to generate"
    )
    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
