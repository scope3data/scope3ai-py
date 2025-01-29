import yaml


class GenerateClientCommands:
    def __init__(self, api_file: str):
        with open(api_file, "r") as f:
            self.openapi = yaml.safe_load(f)
        self.generate()

    def generate(self):
        for path, operations in self.openapi["paths"].items():
            for method, operation in operations.items():
                self.generate_command(path, method, operation)

    def generate_command(self, path: str, method: str, operation: dict):
        print(f"generate_command: {path}, {method}")
        funcname = self.normalize_path_for_function(path, method)
        # funcparams = []
        print(f"def {funcname}(self): pass")

        # # build parameters
        # parameters = operation.get("parameters", [])
        # for argname, parameter in parameters:
        #     argtype = self.normalize_parameter_type(parameter)

        # print(funcparams, argtype)

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
