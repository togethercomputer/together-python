from setuptools import setup, find_packages

REQUIRED_PKGS = [
    "typer",
    "requests",
]

QUALITY_REQUIRE = ["black~=23.1", "ruff>=0.0.241,<=0.0.259"]

EXTRAS_REQUIRE = {
    "quality": QUALITY_REQUIRE,
}

setup(
    name="together",
    author="togethercomputer",
    author_email="support@together.xyz",
    description="Together is a python client for Together's Cloud Platform",
    version="0.0.1",
    scripts=["together/bin/together"],
    package_dir={"together": "together"},
    packages=find_packages(),
    install_requires=REQUIRED_PKGS,
    extras_require=EXTRAS_REQUIRE,
    python_requires=">=3.8.11",
)
