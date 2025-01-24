# chat-async.py
import asyncio

from huggingface_hub import AsyncInferenceClient

from scope3ai import Scope3AI
from scope3ai.tracers.huggingface.chat import HUGGING_FACE_CHAT_TASK


async def main(
    model: str | None, message: str, role: str, max_tokens: int, debug: bool = False
):
    client = AsyncInferenceClient()
    scope3 = Scope3AI.init()
    model_to_use = (
        model if model else client.get_recommended_model(HUGGING_FACE_CHAT_TASK)
    )

    with scope3.trace() as tracer:
        response = await client.chat_completion(
            model=model_to_use,
            messages=[{"role": role, "content": message}],
            max_tokens=max_tokens,
        )
        print(response)
        impact = tracer.impact()
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Hugging Face Chat Completion with Environmental Impact Tracking"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Model to use (default: recommended model)",
    )
    parser.add_argument(
        "--message",
        type=str,
        default="Hello World!",
        help="Message to send to the chat model",
    )
    parser.add_argument(
        "--role",
        type=str,
        default="user",
        help="Role for the message (user, system, or assistant)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=15,
        help="Maximum number of tokens to generate",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode", default=False
    )
    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
