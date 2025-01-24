import asyncio
from pathlib import Path
from scope3ai import Scope3AI
from litellm import aspeech


async def main(
    model: str, text: str, voice: str, output: Path, api_key: str | None = None
):
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        response = await aspeech(model=model, input=text, voice=voice, api_key=api_key)
        # Handle response and save to output file
        # Implementation depends on LiteLLM's response format
        print(response)
        impact = tracer.impact()
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="LiteLLM Text-to-Speech with Environmental Impact Tracking"
    )
    parser.add_argument(
        "--model", type=str, default="tts-1", help="Model to use for speech synthesis"
    )
    parser.add_argument(
        "--text",
        type=str,
        default="Hello, this is a test of text-to-speech conversion.",
        help="Text to convert to speech",
    )
    parser.add_argument(
        "--voice", type=str, default="alloy", help="Voice to use for synthesis"
    )
    parser.add_argument(
        "--output", type=Path, default=Path("output.mp3"), help="Output audio file path"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="API key (optional if set in environment)",
        default=None,
    )
    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
