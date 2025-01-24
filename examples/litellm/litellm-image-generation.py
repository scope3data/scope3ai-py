from scope3ai import Scope3AI
from litellm import image_generation

DESCRIPTION = "LiteLLM Image Generation with Environmental Impact Tracking"

ARGUMENTS = [
    {
        "name_or_flags": "--model",
        "type": str,
        "default": "dall-e-3",
        "help": "Model to use for image generation",
    },
    {
        "name_or_flags": "--prompt",
        "type": str,
        "default": "A beautiful sunset over mountains",
        "help": "Prompt for image generation",
    },
    {
        "name_or_flags": "--size",
        "type": str,
        "default": "1024x1024",
        "help": "Size of the generated image",
    },
    {
        "name_or_flags": "--api-key",
        "type": str,
        "help": "API key (optional if set in environment)",
        "default": None,
    },
]


def main(model: str, prompt: str, size: str, api_key: str | None = None):
    scope3 = Scope3AI.init()

    with scope3.trace() as tracer:
        response = image_generation(
            model=model, prompt=prompt, size=size, api_key=api_key
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
