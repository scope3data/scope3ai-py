from scope3ai import Scope3AI
from openai import OpenAI


def interact() -> None:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello world"}],
        stream=False,
    )
    return response


if __name__ == "__main__":
    scope3 = Scope3AI.init(enable_debug_logging=True)

    # 1. Impact calculation are done via the Scope3AI API in background
    # so you need to wait for the impact to be calculated
    response = interact()
    response.scope3ai.wait_impact()
    print(response.scope3ai.impact)

    # 2. A tracer will automatically wait for the impact response
    with scope3.trace() as tracer:
        response = interact()
        impact = tracer.impact()
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")

    # 3. A tracer can be used to calculate the impact of multiple requests
    with scope3.trace() as tracer:
        response = interact()
        response = interact()
        impact = tracer.impact()
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")
