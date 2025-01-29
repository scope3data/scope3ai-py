import io
from pathlib import Path

import yaml


class GenerateClientCommands:
    def __init__(self, spec: str, output_filename: Path):
        with open(spec, "r") as f:
            self.openapi = yaml.safe_load(f)

        self.output = io.StringIO()
        self.generate()

        output_filename.write_text(self.output.getvalue())
        import subprocess
        subprocess.run(["ruff", "format", str(output_filename)], check=True)

    def generate(self):
        for path, operations in self.openapi["paths"].items():
            # Extract path parameters if they exist
            path_params = []
            if "parameters" in operations:
                path_params = operations["parameters"]

            # Process each operation method
            for method, operation in operations.items():
                if method == "parameters":
                    continue
                self.generate_command(path, method, operation, path_params)

    def generate_command(
        self, path: str, method: str, operation: dict, path_params: list
    ):
        if "operationId" not in operation:
            raise ValueError(f"No operationId found for {method} {path}")
        funcname = self.normalize_operation_id(operation["operationId"])
        params = []

        # Handle path parameters first
        for parameter in path_params:
            param_name = self.normalize_name(parameter["name"])
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
            param_name = self.normalize_name(parameter["name"])
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

        # Extract return type from success response (200/201/204)
        return_type = None
        responses = operation.get("responses", {})
        for status in ["200", "201", "204"]:
            if status in responses:
                if status == "204":  # No content
                    return_type = "None"
                    break
                response_schema = (
                    responses[status]
                    .get("content", {})
                    .get("application/json", {})
                    .get("schema", {})
                )
                if "$ref" in response_schema:
                    return_type = response_schema["$ref"].split("/")[-1]
                    break

        if return_type is None:
            raise ValueError(f"No 200/201/204 response found for {method} {path}")

        # Add with_response parameter
        params.append("with_response: Optional[bool] = True")

        params_str = ", ".join(["self"] + params)
        return_annotation = f" -> {return_type}" if return_type else ""

        # Generate function body
        body = [
            f"def {funcname}({params_str}){return_annotation}:",
            f'    """{operation.get("summary", "")}\n    """',
        ]

        # Add params dict only if we have query parameters
        has_query_params = any(param.get("in") == "query" for param in parameters)
        if has_query_params:
            body.append("    params = {}")
            for param in parameters:
                if param.get("in") == "query":
                    name = self.normalize_name(param["name"])
                    body.append(f"    if {name} is not None:")
                    body.append(f'        params["{param["name"]}"] = {name}')

        # Build execute_request call
        execute_args = [f'        "{path}"', f'        method="{method.upper()}"']

        if has_query_params:
            execute_args.append("        params=params")
        if "requestBody" in operation:
            execute_args.append("        json=content")
        if return_type and return_type != "None":
            execute_args.append(f"        response_model={return_type}")
        execute_args.append("        with_response=with_response")

        body.append("    return self.execute_request(")
        body.append(",\n".join(execute_args))
        body.append("    )")

        self.output.write("\n".join(body) + "\n\n")

    def normalize_name(self, name: str) -> str:
        """Convert camelCase to snake_case"""
        import re

        # Insert underscore between camelCase
        name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
        # Convert to lowercase
        return name.lower()

    def normalize_operation_id(self, operation_id: str) -> str:
        """Convert camelCase operationId to snake_case function name"""
        return self.normalize_name(operation_id)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate client commands from OpenAPI spec"
    )
    parser.add_argument("spec", type=str, help="OpenAPI spec file")
    parser.add_argument(
        "output",
        type=str,
        help="Output Python file",
    )
    args = parser.parse_args()

    generator = GenerateClientCommands(args.spec, Path(args.output))
