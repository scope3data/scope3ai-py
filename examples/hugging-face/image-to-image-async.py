# image-to-image-async.py
import asyncio
from pathlib import Path
from huggingface_hub import AsyncInferenceClient
from scope3ai import Scope3AI
from scope3ai.tracers.huggingface.image_to_image import HUGGING_FACE_IMAGE_TO_IMAGE_TASK


async def main(model: str | None, image_path: Path, prompt: str, debug: bool = False):
    client = AsyncInferenceClient()
    scope3 = Scope3AI.init()

    model_to_use = (
        model
        if model
        else await client.get_recommended_model(HUGGING_FACE_IMAGE_TO_IMAGE_TASK)
    )

    with scope3.trace() as tracer:
        with open(image_path, "rb") as f:
            response = await client.image_to_image(
                model=model_to_use,
                image=f,
                prompt=prompt,
            )
        print("Image to Image Response:", response)
        impact = tracer.impact(response)
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Hugging Face Image-to-Image Transformation with Environmental Impact Tracking"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Model to use (default: recommended model)",
    )
    parser.add_argument(
        "--image-path", type=Path, required=True, help="Path to the input image file"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="Make it look like a watercolor painting",
        help="Prompt describing the desired transformation",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode", default=False
    )
    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
