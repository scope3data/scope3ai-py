from scope3ai import Scope3AI
from anthropic import Anthropic


def main():
    client = Anthropic()
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        with client.messages.stream(
            model="claude-3-5-sonnet-latest",
            messages=[{"role": "user", "content": "Hello!"}],
            max_tokens=100,
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
            print()

            impact = tracer.impact()
            print(impact)
            print(f"Total Energy Wh: {impact.total_energy_wh}")
            print(f"Total GCO2e: {impact.total_gco2e}")
            print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    main()
