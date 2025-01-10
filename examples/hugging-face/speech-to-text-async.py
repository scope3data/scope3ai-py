import argparse
import asyncio

from huggingface_hub import AsyncInferenceClient
from scope3ai import Scope3AI
from scope3ai.tracers.huggingface.speech_to_text import HUGGING_FACE_SPEECH_TO_TEXT_TASK


async def main(audio_path, model):
    client = AsyncInferenceClient()
    scope3 = Scope3AI.init()
    if not model:
        model = await client.get_recommended_model(HUGGING_FACE_SPEECH_TO_TEXT_TASK)

    with scope3.trace() as tracer:
        # Replace `audio_path` with the path to your audio file
        with open(audio_path, "rb") as f:
            response = await client.automatic_speech_recognition(
                model=model,
                audio=f,
            )
        print("Automatic Speech Recognition Response:", response)
        impact = tracer.impact(response)
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run speech-to-text transformation with environmental impact tracing."
    )
    parser.add_argument("--audio_path", type=str, help="Path to the input audio file.")
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Hugging Face model to use. Defaults to the recommended model.",
    )
    args = parser.parse_args()

    asyncio.run(main(args.audio_path, args.model))
