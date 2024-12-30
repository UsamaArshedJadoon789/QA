from setuptools import setup

setup(
    name="halal-compliance-backend",
    version="0.1.0",
    packages=["halal_compliance_backend"],
    install_requires=[
        "fastapi==0.109.0",
        "uvicorn==0.27.0",
        "numpy==1.26.3",
        "matplotlib==3.8.2",
        "python-multipart==0.0.6"
    ],
)
