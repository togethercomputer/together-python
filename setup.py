from setuptools import setup, find_packages

setup(
    name="together",
    author="togethercomputer",
    author_email="support@together.xyz",
    description="Together cli is a tool to help you join together computer",
    version="0.0.84",
    scripts=["together/bin/together"],
    package_dir={"together": "together"},
    packages=find_packages(),
    install_requires=[
        "typer",
        "requests",
    ],
)
