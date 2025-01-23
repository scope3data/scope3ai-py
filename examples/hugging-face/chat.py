import asyncio

from huggingface_hub import InferenceClient

from scope3ai import Scope3AI
from scope3ai.tracers.huggingface.chat import HUGGING_FACE_CHAT_TASK

DESCRIPTION = "Hugging Face Chat Completion with Environmental Impact Tracking"

ARGUMENTS = [
    {
        "name_or_flags": "--model",
        "type": str,
        "help": "Model to use for chat completion (if not specified, will use recommended model)",
        "default": None,
    },
    {
        "name_or_flags": "--message",
        "type": str,
        "default": "Hello World!",
        "help": "Message to send to the chat model",
    },
    {
        "name_or_flags": "--role",
        "type": str,
        "default": "user",
        "help": "Role for the message (user, system, or assistant)",
    },
    {
        "name_or_flags": "--max-tokens",
        "type": int,
        "default": 15,
        "help": "Maximum number of tokens to generate",
    },
]


async def main(model: str | None, message: str, role: str, max_tokens: int):
    client = InferenceClient()
    # Use provided model or get recommended model
    model_to_use = (
        model if model else client.get_recommended_model(HUGGING_FACE_CHAT_TASK)
    )
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        response = client.chat_completion(
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

    parser = argparse.ArgumentParser(description=DESCRIPTION)
    for argument in ARGUMENTS:
        parser.add_argument(**argument)
    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
