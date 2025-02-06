from anthropic import Anthropic

from scope3ai import Scope3AI


def main(model: str, message: str, max_tokens: int, api_key: str | None = None):
    client = Anthropic(api_key=api_key) if api_key else Anthropic()
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        response = client.messages.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            max_tokens=max_tokens,
        )
        print(response.scope3ai)
        print(response.content[0].text.strip())

        impact = tracer.impact()
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Anthropic Claude Async Chat Completion with Environmental Impact Tracking"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="claude-3-5-sonnet-20241022",
        help="Model to use for chat completion",
    )
    parser.add_argument(
        "--message", type=str, default="Hello!", help="Message to send to Claude"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=100,
        help="Maximum number of tokens in the response",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Anthropic API key (optional if set in environment)",
        default=None,
    )
    args = parser.parse_args()
    main(**vars(args))
