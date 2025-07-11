#!/usr/bin/env python3
"""
Setup script para index2md
"""

from setuptools import setup, find_packages
import os

# Leer el README
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Leer requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="index2md",
    version="1.0.0",
    author="index2md",
    description="Script para generar índices y documentación",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/index2md",
    py_modules=["index2md"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "index2md=index2md:main",
        ],
    },
    keywords="markdown, documentation, index, yaml, pandoc",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/index2md/issues",
        "Source": "https://github.com/yourusername/index2md",
    },
) 