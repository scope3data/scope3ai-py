import asyncio

from huggingface_hub import InferenceClient
from scope3ai import Scope3AI
from scope3ai.tracers.huggingface.speech_to_text import HUGGING_FACE_SPEECH_TO_TEXT_TASK


async def main():
    client = InferenceClient()
    scope3 = Scope3AI.init()
    model = client.get_recommended_model(HUGGING_FACE_SPEECH_TO_TEXT_TASK)

    with scope3.trace() as tracer:
        # Replace `audio_path` with the path to your audio file
        audio_path = "path/to/your/audio.wav"
        with open(audio_path, "rb") as f:
            response = client.automatic_speech_recognition(
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
    asyncio.run(main())
