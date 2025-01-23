# speech-to-text.py
import asyncio
from pathlib import Path
from huggingface_hub import InferenceClient
from scope3ai import Scope3AI
from scope3ai.tracers.huggingface.speech_to_text import HUGGING_FACE_SPEECH_TO_TEXT_TASK

DESCRIPTION = (
    "Hugging Face Speech-to-Text Transcription with Environmental Impact Tracking"
)

ARGUMENTS = [
    {
        "name_or_flags": "--model",
        "type": str,
        "default": None,
        "help": "Model to use (default: recommended model)",
    },
    {
        "name_or_flags": "--audio-path",
        "type": Path,
        "required": True,
        "help": "Path to the input audio file",
    },
    {
        "name_or_flags": "--debug",
        "action": "store_true",
        "help": "Enable debug mode",
        "default": False,
    },
]


async def main(model: str | None, audio_path: Path, debug: bool = False):
    client = InferenceClient()
    scope3 = Scope3AI.init()
    model_to_use = (
        model
        if model
        else client.get_recommended_model(HUGGING_FACE_SPEECH_TO_TEXT_TASK)
    )

    with scope3.trace() as tracer:
        with open(audio_path, "rb") as f:
            response = client.automatic_speech_recognition(
                model=model_to_use,
                audio=f,
            )
        print("Automatic Speech Recognition Response:", response)
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
