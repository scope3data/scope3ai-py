"""
Example of using a asynchronous API client to interact with the Scope3 AI API.

This script outputs:

```
Listing GPUs
gpus=[Gpu(name='AMD MI300X', id='mi300x', max_power_w=750.0, embodied_emissions_kgco2e=190.0, embodied_water_mlh2o=11700.0, performance_ratio_to_h200=0.9), Gpu(name='NVIDIA H100', id='h100', max_power_w=700.0, embodied_emissions_kgco2e=176.0, embodied_water_mlh2o=11200.0, performance_ratio_to_h200=1.0), Gpu(name='NVIDIA A100 80GB', id='a100_80gb', max_power_w=400.0, embodied_emissions_kgco2e=165.0, embodied_water_mlh2o=10125.0, performance_ratio_to_h200=0.6), Gpu(name='NVIDIA A10', id='a10', max_power_w=150.0, embodied_emissions_kgco2e=75.0, embodied_water_mlh2o=7854.0, performance_ratio_to_h200=0.2), Gpu(name='NVIDIA L4', id='l4', max_power_w=72.0, embodied_emissions_kgco2e=66.0, embodied_water_mlh2o=7280.0, performance_ratio_to_h200=0.15), Gpu(name='AMD MI250X', id='mi250x', max_power_w=560.0, embodied_emissions_kgco2e=156.0, embodied_water_mlh2o=10530.0, performance_ratio_to_h200=0.7), Gpu(name='NVIDIA H200', id='h200', max_power_w=700.0, embodied_emissions_kgco2e=176.0, embodied_water_mlh2o=11200.0, performance_ratio_to_h200=1.0), Gpu(name='NVIDIA A100 40GB', id='a100_40gb', max_power_w=400.0, embodied_emissions_kgco2e=165.0, embodied_water_mlh2o=10125.0, performance_ratio_to_h200=0.55), Gpu(name='NVIDIA L40', id='l40', max_power_w=300.0, embodied_emissions_kgco2e=112.0, embodied_water_mlh2o=8330.0, performance_ratio_to_h200=0.4)]
Sending impact
has_errors=False rows=[ImpactResponseRow(fine_tuning_impact=ImpactMetrics(usage_energy_wh=0.0, usage_emissions_gco2e=0.0, usage_water_ml=0.0, embodied_emissions_gco2e=0.0, embodied_water_ml=0.0, errors=None), inference_impact=ImpactMetrics(usage_energy_wh=38.23809, usage_emissions_gco2e=31.672613, usage_water_ml=209.16235, embodied_emissions_gco2e=0.7661967, embodied_water_ml=0.33086538, errors=None), training_impact=ImpactMetrics(usage_energy_wh=0.39138946, usage_emissions_gco2e=0.15655577, usage_water_ml=0.5870842, embodied_emissions_gco2e=0.15655577, embodied_water_ml=0.39138946, errors=None), total_impact=ImpactMetrics(usage_energy_wh=38.62948, usage_emissions_gco2e=31.829168, usage_water_ml=209.74944, embodied_emissions_gco2e=0.9227525, embodied_water_ml=0.7222549, errors=None), error=None)]
```
"""

from scope3ai.v1.client import AsyncClient

# api_key is taken from the environment variable SCOPE3AI_API_KEY
client = AsyncClient()


async def list_gpus():
    print("Listing GPUs")
    response = await client.gpu()
    print(response)


async def send_impact():
    from scope3ai.v1.types import ImpactRequestRow, Model

    print("Sending impact")
    impact = ImpactRequestRow(
        model=Model(id="gpt_4o"), input_tokens=100, output_tokens=100
    )
    response = await client.impact(rows=[impact])
    print(response)


if __name__ == "__main__":
    import asyncio

    async def main():
        await list_gpus()
        await send_impact()

    asyncio.run(main())
