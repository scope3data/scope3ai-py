# text-to-speech.py
import asyncio
from pathlib import Path
from huggingface_hub import InferenceClient
from scope3ai import Scope3AI
from scope3ai.tracers.huggingface.text_to_speech import HUGGING_FACE_TEXT_TO_SPEECH_TASK

DESCRIPTION = "Hugging Face Text-to-Speech Synthesis with Environmental Impact Tracking"

ARGUMENTS = [
    {
        "name_or_flags": "--model",
        "type": str,
        "default": None,
        "help": "Model to use (default: recommended model)",
    },
    {
        "name_or_flags": "--text",
        "type": str,
        "default": "Hello, welcome to the future of AI!",
        "help": "Text to convert to speech",
    },
    {
        "name_or_flags": "--output-path",
        "type": Path,
        "default": Path("output.wav"),
        "help": "Path to save the output audio file",
    },
    {
        "name_or_flags": "--debug",
        "action": "store_true",
        "help": "Enable debug mode",
        "default": False,
    },
]


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

    parser = argparse.ArgumentParser(description=DESCRIPTION)
    for argument in ARGUMENTS:
        parser.add_argument(**argument)
    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
