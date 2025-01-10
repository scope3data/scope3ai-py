import asyncio
import argparse

from huggingface_hub import AsyncInferenceClient
from scope3ai import Scope3AI
from scope3ai.tracers.huggingface.image_to_image import HUGGING_FACE_IMAGE_TO_IMAGE_TASK


async def main(image_path, model):
    client = AsyncInferenceClient()
    scope3 = Scope3AI.init()
    if not model:
        model = await client.get_recommended_model(HUGGING_FACE_IMAGE_TO_IMAGE_TASK)

    with scope3.trace() as tracer:
        # Replace `image_path` with the path to your image file
        with open(image_path, "rb") as f:
            response = await client.image_to_image(
                model=model,
                image=f,
                prompt="Make it look like a watercolor painting",
            )
        print("Image to Image Response:", response)
        impact = tracer.impact(response)
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run image-to-image transformation with environmental impact tracing."
    )
    parser.add_argument("--image-path", type=str, help="Path to the input image file.")
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Hugging Face model to use. Defaults to the recommended model.",
    )
    args = parser.parse_args()

    asyncio.run(main(args.image_path, args.model))
