import yaml


class GenerateClientCommands:
    def __init__(self, api_file: str):
        with open(api_file, "r") as f:
            self.openapi = yaml.safe_load(f)
        self.generate()

    def generate(self):
        for path, operations in self.openapi["paths"].items():
            # Extract path parameters if they exist
            path_params = []
            if "parameters" in operations:
                path_params = operations["parameters"]
            
            # Process each operation method
            for method, operation in operations.items():
                if method != "parameters":  # Skip the parameters method itself
                    self.generate_command(path, method, operation, path_params)

    def generate_command(self, path: str, method: str, operation: dict, path_params: list):
        print(f"generate_command: {path}, {method}")
        print(operation)
        funcname = self.normalize_path_for_function(path, method)
        params = []

        # Handle path parameters first
        for parameter in path_params:
            param_name = parameter["name"]
            schema = parameter.get("schema", {})
            if "$ref" in schema:
                param_type = schema["$ref"].split("/")[-1]
            else:
                param_type = schema.get("type", "Any")
            # Path parameters are always required
            params.append(f"{param_name}: {param_type}")

        # Handle operation-specific parameters
        parameters = operation.get("parameters", [])
        for parameter in parameters:
            param_name = parameter["name"]
            schema = parameter.get("schema", {})
            if "$ref" in schema:
                param_type = schema["$ref"].split("/")[-1]
            else:
                param_type = schema.get("type", "Any")

            if not parameter.get("required", False):
                param_type = f"Optional[{param_type}]"
                params.append(f"{param_name}: {param_type} = None")
            else:
                params.append(f"{param_name}: {param_type}")

        # Handle request body
        if "requestBody" in operation:
            content = operation["requestBody"]["content"]
            if "application/json" in content:
                schema = content["application/json"]["schema"]
                if "$ref" in schema:
                    content_type = schema["$ref"].split("/")[-1]
                else:
                    content_type = "dict"
                params.append(f"content: {content_type}")

        params_str = ", ".join(["self"] + params)
        print(f"def {funcname}({params_str}): pass")

    def normalize_path_for_function(self, path: str, method: str):
        # examples:
        # /node/{nodeId} get -> get_node
        # /model/{modelId} post -> post_model
        # /model/{modelId}/alias get -> get_model_alias
        # /model/{modelId}/alias/[alias} delete -> delete_model_alias
        function_name = ""
        for part in path.split("/"):
            if part and "{" not in part:
                function_name += f"_{part}"

        method = method.lower()
        function_name = f"{method}{function_name}"
        return function_name.strip("_")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate client commands from OpenAPI spec"
    )
    parser.add_argument("api_file", type=str, help="OpenAPI spec file")
    args = parser.parse_args()

    generator = GenerateClientCommands(args.api_file)
