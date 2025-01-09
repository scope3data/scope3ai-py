import asyncio

from huggingface_hub import InferenceClient
from scope3ai import Scope3AI
from scope3ai.tracers.huggingface.image_to_image import HUGGING_FACE_IMAGE_TO_IMAGE_TASK


async def main():
    client = InferenceClient()
    scope3 = Scope3AI.init()
    model = client.get_recommended_model(HUGGING_FACE_IMAGE_TO_IMAGE_TASK)

    with scope3.trace() as tracer:
        # Replace `image_path` with the path to your image file
        image_path = "path/to/your/image.jpg"
        with open(image_path, "rb") as f:
            response = client.image_to_image(
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
    asyncio.run(main())
