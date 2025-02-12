#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


OPENAPI_SPEC_URL = "https://raw.githubusercontent.com/togethercomputer/openapi/main/openapi.yaml"
OUTPUT_DIR = Path(__file__).parent.parent / "src" / "together" / "generated"
GENERATOR_JAR_URL = "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.11.0/openapi-generator-cli-7.11.0.jar"
GENERATOR_JAR = Path(__file__).parent / "openapi-generator-cli.jar"


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a command and optionally check its return code."""
    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def download_file(url: str, target: Path) -> None:
    """Download a file"""

    print(f"Downloading {url} to {target}")
    run_command(["wget", "-O", str(target), url])


def main() -> None:
    # Download OpenAPI spec
    spec_file = Path(__file__).parent / "openapi.yaml"
    download_file(OPENAPI_SPEC_URL, spec_file)

    # Run formatter on the spec for better merge conflict handling
    run_command(["npx", "-y", "prettier", "--write", str(spec_file)])

    # Download generator if needed
    download_file(GENERATOR_JAR_URL, GENERATOR_JAR)

    # Delete existing generated code
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate client code
    cmd = [
        "java",
        "-jar",
        str(GENERATOR_JAR),
        "generate",
        "-i",
        str(spec_file),
        "-g",
        "python",
        "-o",
        str(OUTPUT_DIR),
        "--package-name=together.generated",
        "--git-repo-id=together-python",
        "--git-user-id=togethercomputer",
        "--additional-properties=packageUrl=https://github.com/togethercomputer/together-python",
        "--additional-properties=library=asyncio",
        "--additional-properties=generateSourceCodeOnly=true",
    ]

    print("Generating client code...")
    result = run_command(cmd, check=False)

    if result.returncode != 0:
        print("Error generating client code:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    # Move files from nested directory to target directory
    nested_dir = OUTPUT_DIR / "together" / "generated"
    if nested_dir.exists():
        print("Moving files from nested directory...")
        # Move all contents to parent directory
        for item in nested_dir.iterdir():
            shutil.move(str(item), str(OUTPUT_DIR / item.name))
        # Clean up empty directories
        shutil.rmtree(OUTPUT_DIR / "together", ignore_errors=True)

    print("Successfully generated client code")


if __name__ == "__main__":
    main()
