from pathlib import Path

from setuptools import find_packages, setup

setup(
    name="facpu-assembler",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "facpu = facpu.cli:main",
        ],
    },
    install_requires=["colored", "pyperclip", "factorio-draftsman"],
    author="Joel Cutler",
    description="facPU assembler",
    long_description=(Path(__file__).parent / "README.md").read_text("utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/jcbyte/facPU",
    python_requires=">=3.6",
)
