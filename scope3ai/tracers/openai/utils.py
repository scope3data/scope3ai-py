from typing import Any


class BaseModelResponse:
    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        model_dump_response = super().model_dump()
        del model_dump_response["scope3ai"]
        return model_dump_response
