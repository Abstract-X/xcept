import setuptools
from pathlib import Path


def get_long_description() -> str:
    path = Path(__file__).parent / "README.md"

    with path.open(encoding="UTF-8") as stream:
        long_description = stream.read()

    return long_description


setuptools.setup(
    name="xcept",
    version="3.0.0",
    packages=setuptools.find_packages(exclude=("tests",)),
    url="https://github.com/Abstract-X/xcept",
    author="Abstract-X",
    author_email="abstract-x-mail@protonmail.com",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ]
)
