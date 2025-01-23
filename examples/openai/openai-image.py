from openai import OpenAI

from scope3ai import Scope3AI

DESCRIPTION = "OpenAI Image Generation with Environmental Impact Tracking"

ARGUMENTS = [
    {
        "name_or_flags": "--model",
        "type": str,
        "default": "dall-e-2",
        "help": "Model to use for image generation",
    },
    {
        "name_or_flags": "--prompt",
        "type": str,
        "default": "A beautiful landscape",
        "help": "Prompt for image generation",
    },
    {
        "name_or_flags": "--n",
        "type": int,
        "default": 1,
        "help": "Number of images to generate",
    },
    {
        "name_or_flags": "--size",
        "type": str,
        "default": "512x512",
        "help": "Size of the generated image",
    },
]


def main(model: str, prompt: str, n: int, size: str):
    client = OpenAI()
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        response = client.images.generate(
            model=model,
            prompt=prompt,
            n=n,
            size=size,
        )
        print(response.data[0].url)

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
