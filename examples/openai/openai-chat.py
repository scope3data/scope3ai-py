from scope3ai import Scope3AI
from openai import OpenAI


def main(model: str, message: str, role: str):
    client = OpenAI()
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": role, "content": message}],
        )
        print(response.choices[0].message.content.strip())

        impact = tracer.impact()
        print(impact)
        print(f"Total Energy Wh: {impact.total_energy_wh}")
        print(f"Total GCO2e: {impact.total_gco2e}")
        print(f"Total MLH2O: {impact.total_mlh2o}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenAI Chat Completion with Environmental Impact Tracking"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-3.5-turbo",
        help="Model to use for chat completion",
    )
    parser.add_argument(
        "--message",
        type=str,
        default="Hello!",
        help="Message to send to the chat model",
    )
    parser.add_argument(
        "--role",
        type=str,
        default="user",
        help="Role for the message (user, system, or assistant)",
    )
    args = parser.parse_args()
    main(**vars(args))
