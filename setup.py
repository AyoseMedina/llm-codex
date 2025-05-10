import os
from setuptools import setup, find_packages

setup(
    name="llm-codex",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "llm-codex = llm_codex.main:main"
        ]
    },
    author="Ayose Medina",
    description="CLI para generar, editar y ejecutar código con LLM Studio desde cualquier carpeta.",
    long_description=open("README.md", encoding="utf-8").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.6",
)
