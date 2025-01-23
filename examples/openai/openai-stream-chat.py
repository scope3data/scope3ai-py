from scope3ai import Scope3AI
from openai import OpenAI

DESCRIPTION = "OpenAI Streaming Chat Completion with Environmental Impact Tracking"

ARGUMENTS = [
    {
        "name_or_flags": "--model",
        "type": str,
        "default": "gpt-3.5-turbo",
        "help": "Model to use for chat completion",
    },
    {
        "name_or_flags": "--message",
        "type": str,
        "default": "Hello!",
        "help": "Message to send to the chat model",
    },
    {
        "name_or_flags": "--role",
        "type": str,
        "default": "user",
        "help": "Role for the message (user, system, or assistant)",
    },
    {
        "name_or_flags": "--no-stream",
        "action": "store_false",
        "dest": "stream",
        "help": "Disable streaming mode",
        "default": True,
    },
]


def main(model: str, message: str, role: str, stream: bool):
    client = OpenAI()
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": role, "content": message}],
            stream=stream,
        )

        if stream:
            for event in response:
                if not event.choices:
                    continue
                print(event.choices[0].delta.content, end="", flush=True)
            print()

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
    main(**vars(args))
