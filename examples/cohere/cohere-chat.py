import cohere
from scope3ai import Scope3AI

DESCRIPTION = "Cohere Chat Completion with Environmental Impact Tracking"

ARGUMENTS = [
    {
        "name_or_flags": "--message",
        "type": str,
        "default": "Hello!",
        "help": "Message to send to the chat model",
    },
    {
        "name_or_flags": "--max-tokens",
        "type": int,
        "default": 100,
        "help": "Maximum number of tokens in the response",
    },
    {
        "name_or_flags": "--api-key",
        "type": str,
        "help": "Cohere API key (optional if set in environment)",
        "default": None,
    },
]


def main(message: str, max_tokens: int, api_key: str | None = None):
    scope3 = Scope3AI.init()
    co = cohere.Client(api_key=api_key) if api_key else cohere.Client()

    with scope3.trace() as tracer:
        response = co.chat(message=message, max_tokens=max_tokens)
        print(response)

        impact = tracer.impact()
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=DESCRIPTION)
    for argument in ARGUMENTS:
        parser.add_argument(**argument)
    args = parser.parse_args()
    main(**vars(args))
