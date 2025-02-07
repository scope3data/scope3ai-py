import cohere

from scope3ai import Scope3AI


def main(
    model: str, message: str, role: str, max_tokens: int, api_key: str | None = None
):
    scope3 = Scope3AI.init()
    co = cohere.ClientV2(api_key=api_key) if api_key else cohere.ClientV2()

    with scope3.trace() as tracer:
        stream = co.chat_stream(
            model=model,
            messages=[{"role": role, "content": message}],
            max_tokens=max_tokens,
        )
        for event in stream:
            if (
                hasattr(event, "delta")
                and hasattr(event.delta, "message")
                and event.delta.message.content
            ):
                print(event.delta.message.content.text, end="", flush=True)

        impact = tracer.impact()
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Cohere v2 Streaming Chat Completion with Environmental Impact Tracking"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="command-r-plus-08-2024",
        help="Model to use for chat completion",
    )
    parser.add_argument(
        "--message",
        type=str,
        default="Hello world!",
        help="Message to send to the chat model",
    )
    parser.add_argument("--role", type=str, default="user", help="Role for the message")
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=100,
        help="Maximum number of tokens in the response",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Cohere API key (optional if set in environment)",
        default=None,
    )
    args = parser.parse_args()
    main(**vars(args))
