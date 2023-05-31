from setuptools import setup, find_packages

setup(
    name="together",
    author="togethercomputer",
    author_email="support@together.xyz",
    description="Together is a python client for Together's Cloud Platform",
    version="0.0.1",
    scripts=["together/bin/together"],
    package_dir={"together": "together"},
    packages=find_packages(),
    install_requires=[
        "typer",
        "requests",
    ],
)
