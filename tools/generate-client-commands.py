import io
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import yaml


class GenerateClientCommands:
    # OpenAPI to Python type mapping
    TYPE_MAP = {
        "string": "str",
        "boolean": "bool",
        "integer": "int",
        "number": "float",
        "array": "list",
        "object": "dict",
    }

    def __init__(self, spec: str, output_filename: Path):
        with open(spec, "r") as f:
            self.openapi = yaml.safe_load(f)

        self.output = io.StringIO()

        # Get all unique types used in responses and parameters
        self.used_types = set()
        self.collect_types()

        # Generate the file
        self.generate_header(spec)
        self.generate_imports()
        self.generate_start()
        self.generate()

        output_filename.write_text(self.output.getvalue())

        # Run ruff commands
        self._run_subprocess(["ruff", "check", "--fix", str(output_filename)])
        self._run_subprocess(
            ["ruff", "check", "--select", "I", "--fix", str(output_filename)]
        )
        self._run_subprocess(["ruff", "format", str(output_filename)])

        print(f"Generated {output_filename}")

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

    def generate_header(self, spec_file: str):
        timestamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        header = [
            "# generated by generate-client-commands.py",
            f"#  filename: {Path(spec_file).name}",
            f"#  timestamp: {timestamp}",
            "",
            "",
        ]
        self.output.write("\n".join(header))

    def generate_imports(self):
        imports = [
            "from typing import Any, Optional",
            "",
        ]

        if self.used_types:
            types_import = (
                "from .typesgen import (\n    "
                + ",\n    ".join(sorted(self.used_types))
                + "\n)"
            )
            imports.append(types_import)
            imports.append("")

        self.output.write("\n".join(imports) + "\n\n")

    def generate_start(self):
        content = [
            "class ClientCommands:\n",
            "    def execute_request(self, *args, **kwargs) -> Any:\n",
            "        raise NotImplementedError\n\n",
        ]
        self.output.write("".join(content))

    def collect_types(self):
        """Collect all unique types used in responses and parameters"""
        for path_item in self.openapi["paths"].values():
            # Collect from path parameters
            if "parameters" in path_item:
                self.collect_parameter_types(path_item["parameters"])

            # Collect from operations
            for method, operation in path_item.items():
                if method == "parameters":
                    continue

                # Collect from operation parameters
                if "parameters" in operation:
                    self.collect_parameter_types(operation["parameters"])

                # Collect from request body
                if "requestBody" in operation:
                    self.collect_schema_type(
                        operation["requestBody"]
                        .get("content", {})
                        .get("application/json", {})
                        .get("schema", {})
                    )

                # Collect from responses
                for response in operation.get("responses", {}).values():
                    self.collect_schema_type(
                        response.get("content", {})
                        .get("application/json", {})
                        .get("schema", {})
                    )

    def collect_parameter_types(self, parameters):
        """Helper to collect types from parameters"""
        for param in parameters:
            schema = param.get("schema", {})
            if "$ref" in schema:
                self.used_types.add(schema["$ref"].split("/")[-1])

    def collect_schema_type(self, schema):
        """Helper to collect type from a schema"""
        if "$ref" in schema:
            self.used_types.add(schema["$ref"].split("/")[-1])

    def generate_command(
        self, path: str, method: str, operation: dict, path_params: list
    ):
        if "operationId" not in operation:
            raise ValueError(f"No operationId found for {method} {path}")
        funcname = self.normalize_operation_id(operation["operationId"])
        params = []

        # 1. Handle path parameters first
        for parameter in path_params:
            param_name = self.normalize_name(parameter["name"])
            schema = parameter.get("schema", {})
            if "$ref" in schema:
                param_type = schema["$ref"].split("/")[-1]
            else:
                param_type = self.TYPE_MAP.get(schema.get("type"), "Any")
            # Path parameters are always required
            params.append(f"{param_name}: {param_type}")

        # 2. Handle request body if it exists
        if "requestBody" in operation:
            content = operation["requestBody"]["content"]
            if "application/json" in content:
                schema = content["application/json"]["schema"]
                if "$ref" in schema:
                    content_type = schema["$ref"].split("/")[-1]
                else:
                    content_type = "dict"
                params.append(f"content: {content_type}")

        # 3. Handle query parameters
        parameters = operation.get("parameters", [])
        for parameter in parameters:
            if parameter.get("in") == "query":  # Only process query parameters
                param_name = self.normalize_name(parameter["name"])
                schema = parameter.get("schema", {})
                if "$ref" in schema:
                    param_type = schema["$ref"].split("/")[-1]
                else:
                    param_type = self.TYPE_MAP.get(schema.get("type"), "Any")

                if not parameter.get("required", False):
                    param_type = f"Optional[{param_type}]"
                    params.append(f"{param_name}: {param_type} = None")
                else:
                    params.append(f"{param_name}: {param_type}")

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

        # 4. Add with_response parameter last
        params.append("with_response: Optional[bool] = True")

        params_str = ", ".join(["self"] + params)
        return_annotation = f" -> {return_type}" if return_type else ""

        # Generate function body
        body = [
            f"    def {funcname}({params_str}){return_annotation}:",
            f'        """{operation.get("summary", "")}\n        """',
        ]

        # Add params dict only if we have query parameters
        has_query_params = any(param.get("in") == "query" for param in parameters)
        if has_query_params:
            body.append("        params = {}")
            for param in parameters:
                if param.get("in") == "query":
                    name = self.normalize_name(param["name"])
                    body.append(f"        if {name} is not None:")
                    body.append(f'            params["{param["name"]}"] = {name}')

        # Build execute_request call
        execute_args = [
            f'            "{path}"',
            f'            method="{method.upper()}"',
        ]

        if has_query_params:
            execute_args.append("            params=params")
        if "requestBody" in operation:
            execute_args.append("            json=content")
        if return_type and return_type != "None":
            execute_args.append(f"            response_model={return_type}")
        execute_args.append("            with_response=with_response")

        body.append("        return self.execute_request(")
        body.append(",\n".join(execute_args))
        body.append("        )")

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

    def _run_subprocess(self, cmd: list[str]) -> None:
        """Run a subprocess command and handle errors"""
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            cmdtxt = " ".join(cmd)
            if result.stderr:
                print(f"{cmdtxt}: failed [stderr]:\n{result.stderr}")
            if result.stdout:
                print(f"{cmdtxt} failed [stdout]:\n{result.stdout}")
            raise subprocess.CalledProcessError(
                result.returncode, result.args, result.stdout, result.stderr
            )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate client commands from OpenAPI spec"
    )
    parser.add_argument("spec", type=str, help="OpenAPI spec file")
    parser.add_argument(
        "--output",
        type=str,
        default="scope3ai/api/commandsgen.py",
        help="Output Python file",
    )
    args = parser.parse_args()

    generator = GenerateClientCommands(args.spec, Path(args.output))
