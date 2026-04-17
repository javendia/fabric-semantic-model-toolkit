from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the contents of the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="fabtoolkit",
    version="1.0.0",
    author="Javier Buendía",
    description="Utility library designed to reuse common tasks when working with Microsoft Fabric.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    project_urls={},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Topic :: Microsoft Fabric Development",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.10",
    install_requires=requirements
)