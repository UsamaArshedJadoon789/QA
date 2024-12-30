from setuptools import setup

setup(
    name="halal-compliance-api",
    version="1.0.0",
    py_modules=['main', 'generate_test_data', 'startup'],
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
