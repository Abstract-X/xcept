import setuptools
from pathlib import Path


def get_long_description() -> str:

    path = Path(__file__).parent / "README.md"
    with open(str(path), encoding="UTF-8") as stream:
        long_description = stream.read()

    return long_description


setuptools.setup(
    name="xcept",
    version="0.1.0",
    packages=setuptools.find_packages(exclude=("tests", "docs")),
    url="https://github.com/Abstract-X/xcept",
    author="Abstract-X",
    author_email="abstract-x-mail@protonmail.com",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    python_requires='>=3.8'
)
