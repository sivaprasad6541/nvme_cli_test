#!/usr/bin/env python3
"""Setup script for the C to C++ Conversion Agent."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = requirements_path.read_text().strip().split('\n')
    requirements = [req for req in requirements if req and not req.startswith('#')]

setup(
    name="c-to-cpp-converter",
    version="1.0.0",
    description="Intelligent C to C++ conversion agent with AI-powered analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AI Code Converter Team",
    author_email="dev@converter.ai",
    url="https://github.com/ai-converter/c-to-cpp",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "c2cpp=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: C",
        "Programming Language :: C++",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Compilers",
    ],
    keywords="c c++ conversion code-analysis ai llm modernization",
    project_urls={
        "Bug Reports": "https://github.com/ai-converter/c-to-cpp/issues",
        "Source": "https://github.com/ai-converter/c-to-cpp",
        "Documentation": "https://c-to-cpp-converter.readthedocs.io/",
    },
)