import setuptools
from setuptools import setup, find_packages

setup(
    name="manim_hf_renderer",
    version="0.1.0",
    author="Manim HF Renderer Team",
    author_email="user@example.com",
    description="A tool to render Manim animations using Hugging Face Spaces",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/manim_hf_renderer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.0",
        "tqdm>=4.64.0",
        "python-dotenv>=0.20.0",
        "huggingface-hub>=0.13.0",
        "Pillow>=9.0.0",
        "numpy>=1.22.0",
        "pydantic>=1.10.0",
    ],
    entry_points={
        "console_scripts": [
            "manim-render=render_manim_hf:main",
        ],
    },
)