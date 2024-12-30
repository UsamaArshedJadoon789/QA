from setuptools import setup, find_packages

setup(
    name="halal-compliance-api",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "numpy",
        "matplotlib",
        "pandas",
        "python-multipart",
        "aiofiles"
    ],
    python_requires=">=3.8",
)
