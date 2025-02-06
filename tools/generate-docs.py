import sys
from pathlib import Path

import tomli
from pydoc_markdown import PydocMarkdown
from pydoc_markdown.interfaces import Context


def load_config():
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("Error: pyproject.toml not found")
        sys.exit(1)

    with open(pyproject_path, "rb") as f:
        return tomli.load(f)["tool"]["pydoc-markdown"]


def generate_docs():
    config = load_config()

    for module in config["modules"]["members"]:
        module_config = config.copy()
        module_config["loaders"][0]["module"] = module

        pydoc = PydocMarkdown(module_config)
        pydoc.process(Context(directory=Path.cwd()))


if __name__ == "__main__":
    generate_docs()
