import cohere

from scope3ai import Scope3AI


def main():
    scope3 = Scope3AI.init()
    co = cohere.Client()

    with scope3.trace() as tracer:
        response = co.chat(message="Hello!", max_tokens=100)
        print(response)

        impact = tracer.impact()
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    main()
