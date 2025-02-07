import asyncio
import cohere
from scope3ai import Scope3AI


async def main(message: str, model: str, max_tokens: int, api_key: str | None = None):
    scope3 = Scope3AI.init()
    co = cohere.AsyncClient(api_key=api_key) if api_key else cohere.AsyncClient()

    with scope3.trace() as tracer:
        response = await co.chat(message=message, model=model, max_tokens=max_tokens)
        print(response)

        impact = tracer.impact()
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Cohere Chat Completion with Environmental Impact Tracking"
    )
    parser.add_argument(
        "--message",
        type=str,
        default="Hello!",
        help="Message to send to the chat model",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=100,
        help="Maximum number of tokens in the response",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="command-r",
        help="Model to use for the chat",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Cohere API key (optional if set in environment)",
        default=None,
    )
    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
