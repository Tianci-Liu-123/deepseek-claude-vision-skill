from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="deepseek-claude-vision-skill",
    version="0.1.0",
    author="Tianci Liu",
    description="A complete Claude Code Skill for DeepSeek Vision image recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tianci-Liu-123/deepseek-claude-vision-skill",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "deepseek-vision=src.cli:main",
        ],
    },
)
