import pathlib
from setuptools import setup, find_packages

# Get the directory of this file
HERE = pathlib.Path(__file__).parent

setup(
    name="kamino",
    version="0.0.1",
    description="Kamino Codenames Analysis",
    long_description=(HERE / "README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Thomas Lazor, Eric Nguyen",
    python_requires=">=3.10",
    url="https://gitlab.com/the-flatmates/kamino",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "black",
        "ipykernel",
        "matplotlib",
        "numpy",
        "pytest",
        "spacy",
        "opencv-python",
        "pytesseract",
    ],
)
