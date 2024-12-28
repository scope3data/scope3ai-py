from pathlib import Path

from huggingface_hub import InferenceClient

from scope3ai import Scope3AI


def interact() -> None:
    datadir = Path(__file__).parent / "data"
    client = InferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct")
    response = client.automatic_speech_recognition(
        audio=(datadir / "hello_there.mp3").as_posix()
    )
    return response


if __name__ == "__main__":
    scope3 = Scope3AI.init(enable_debug_logging=True)
    response = interact()
    response.scope3ai.wait_impact()
    print(response.scope3ai.impact)
    with scope3.trace() as tracer:
        response = interact()
        impact = tracer.impact()
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")
    with scope3.trace() as tracer:
        response = interact()
        response = interact()
        impact = tracer.impact()
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")
