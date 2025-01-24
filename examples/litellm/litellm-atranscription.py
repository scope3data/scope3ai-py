import asyncio
from pathlib import Path
from scope3ai import Scope3AI
from litellm import atranscription

DESCRIPTION = (
    "LiteLLM Async Speech-to-Text Transcription with Environmental Impact Tracking"
)

ARGUMENTS = [
    {
        "name_or_flags": "--model",
        "type": str,
        "default": "whisper-1",
        "help": "Model to use for transcription",
    },
    {
        "name_or_flags": "--audio-path",
        "type": Path,
        "required": True,
        "help": "Path to the input audio file",
    },
    {
        "name_or_flags": "--language",
        "type": str,
        "default": None,
        "help": "Language of the audio (optional)",
    },
    {
        "name_or_flags": "--api-key",
        "type": str,
        "help": "API key (optional if set in environment)",
        "default": None,
    },
]


async def main(
    model: str,
    audio_path: Path,
    language: str | None = None,
    api_key: str | None = None,
):
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        with open(audio_path, "rb") as audio_file:
            response = await atranscription(
                model=model, file=audio_file, language=language, api_key=api_key
            )
            print(response.text)

        impact = tracer.impact()
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
