# text-to-speech.py
import asyncio
from pathlib import Path
from huggingface_hub import InferenceClient
from scope3ai import Scope3AI
from scope3ai.tracers.huggingface.text_to_speech import HUGGING_FACE_TEXT_TO_SPEECH_TASK


async def main(model: str | None, text: str, output_path: Path, debug: bool = False):
    client = InferenceClient()
    scope3 = Scope3AI.init()
    model_to_use = (
        model
        if model
        else client.get_recommended_model(HUGGING_FACE_TEXT_TO_SPEECH_TASK)
    )

    with scope3.trace() as tracer:
        response = client.text_to_speech(
            model=model_to_use,
            text=text,
        )
        print("Text to Speech Response:", response)
        impact = tracer.impact(response)
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Hugging Face Text-to-Speech Synthesis with Environmental Impact Tracking"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Model to use (default: recommended model)",
    )
    parser.add_argument(
        "--text",
        type=str,
        default="Hello, welcome to the future of AI!",
        help="Text to convert to speech",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("output.wav"),
        help="Path to save the output audio file",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode", default=False
    )
    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
