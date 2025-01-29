import shutil
import subprocess
import tempfile
from pathlib import Path


def clone_repository(repo_url: str, clone_dir: Path) -> None:
    try:
        subprocess.run(["git", "clone", repo_url, str(clone_dir)], check=True)
        print(f"Repository cloned successfully: {repo_url}")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to clone repository: {e}")


def copy_file(src: Path, dst: Path) -> None:
    try:
        shutil.copy(src, dst)
        print(f"File copied successfully from {src} to {dst}")
    except IOError as e:
        print(f"ERROR: Failed to copy file: {e}")


def patch_aiapi_yaml(filename: Path) -> None:
    def remove_number_of_experts(text):
        print("- Removing 'number_of_experts' from the ImpactRow")
        lines = text.split("\n")
        new_lines = []
        found = False
        for line in lines:
            if "      - number_of_experts" in line:
                found = True
            else:
                new_lines.append(line)
        if not found:
            raise ValueError("ERROR: 'number_of_experts' not found in the file.")
        return "\n".join(new_lines)

    try:
        print(f"Patching aiapi.yaml: {filename}")
        content = filename.read_text()
        content = remove_number_of_experts(content)
        filename.write_text(content)

    except Exception as e:
        print(f"ERROR: Failed to patch aiapi.yaml: {e}")


def run_code_generation() -> None:
    try:
        subprocess.run(
            [
                "datamodel-codegen",
                "--input",
                "tests/api-mocks/aiapi.yaml",
                "--input-file-type",
                "openapi",
                "--output",
                "scope3ai/api/typesgen.py",
                "--output-model-type",
                "pydantic_v2.BaseModel",
                "--use-schema-description",
                "--use-subclass-enum",
                # If we have a field like `x:  Optional[str] = Field(None, ...)
                # And if not passed in the constructor, pyright will give back an issue
                # saying that x is missing. But it's optional ! See
                # https://github.com/pydantic/pydantic/discussions/7379
                "--use-annotated",
            ],
            check=True,
        )
        subprocess.run(["ruff", "format", "scope3ai/api/typesgen.py"], check=True)
        print("Code generation and formatting completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to run code generation or formatting: {e}")


def run_client_commands_generation() -> None:
    try:
        subprocess.run(
            [
                "uv",
                "run",
                "python",
                "-m",
                "tools.generate-client-commands",
                "tests/api-mocks/aiapi.yaml",
            ],
            check=True,
        )
        print("Client commands generation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to generate client commands: {e}")


def main() -> None:
    repo_url = "git@github.com:scope3data/aiapi"
    dst_file = Path("tests/api-mocks/aiapi.yaml")

    with tempfile.TemporaryDirectory() as tmpdirname:
        clone_dir = Path(tmpdirname)
        src_file = clone_dir / "api/api.yaml"

        try:
            clone_repository(repo_url, clone_dir)
            copy_file(src_file, dst_file)
            patch_aiapi_yaml(dst_file)
            run_code_generation()
            run_client_commands_generation()
        except Exception as e:
            print(f"ERROR: An error occurred: {e}")
            shutil.rmtree(clone_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
