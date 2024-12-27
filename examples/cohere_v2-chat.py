import cohere

from scope3ai import Scope3AI


def main():
    scope3 = Scope3AI.init()
    co = cohere.ClientV2()

    with scope3.trace() as tracer:
        response = co.chat(
            model="command-r-plus-08-2024",
            messages=[{"role": "user", "content": "Hello world!"}],
        )
        print(response)

        impact = tracer.impact()
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    main()
