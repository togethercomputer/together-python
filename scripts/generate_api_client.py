#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


OPENAPI_SPEC_URL = (
    "https://raw.githubusercontent.com/togethercomputer/openapi/main/openapi.yaml"
)
# We no longer set OUTPUT_DIR to the src folder for generation.
# Instead, we'll copy the generated client to the target directory.
TARGET_DIR = Path(__file__).parent.parent / "src" / "together" / "generated"
GENERATOR_JAR_URL = "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.11.0/openapi-generator-cli-7.11.0.jar"
GENERATOR_JAR = Path(__file__).parent / "openapi-generator-cli.jar"


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a command and optionally check its return code."""
    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def download_file(url: str, target: Path) -> None:
    """Download a file."""
    print(f"Downloading {url} to {target}")
    run_command(["wget", "-O", str(target), url])


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate Together API client")
    parser.add_argument(
        "--skip-spec-download",
        action="store_true",
        help="Skip downloading the OpenAPI spec file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    spec_file = Path(__file__).parent / "openapi.yaml"

    # Download OpenAPI spec if not skipped.
    if not args.skip_spec_download:
        download_file(OPENAPI_SPEC_URL, spec_file)
        # Format the spec for better merge conflict handling.
        run_command(["npx", "-y", "prettier", "--write", str(spec_file)])
    elif not spec_file.exists():
        print(
            "Error: OpenAPI spec file not found and download was skipped",
            file=sys.stderr,
        )
        sys.exit(1)

    # Download generator if needed.
    download_file(GENERATOR_JAR_URL, GENERATOR_JAR)

    # Create a temporary directory for generation.
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        # Build the generation command.
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
            str(tmp_path),
            "--package-name=together.generated",
            "--git-repo-id=together-python",
            "--git-user-id=togethercomputer",
            "--additional-properties=packageUrl=https://github.com/togethercomputer/together-python",
            "--additional-properties=library=asyncio",
            "--additional-properties=generateSourceCodeOnly=true",
        ]

        print("Generating client code into temporary directory...")
        result = run_command(cmd, check=False)
        if result.returncode != 0:
            print("Error generating client code:", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            sys.exit(1)

        # The generator will create a directory structure like: tmp_dir/together/generated
        generated_dir = tmp_path / "together" / "generated"
        if not generated_dir.exists():
            print("Error: Expected generated directory not found", file=sys.stderr)
            sys.exit(1)

        # Remove any existing generated client code.
        shutil.rmtree(TARGET_DIR, ignore_errors=True)
        TARGET_DIR.parent.mkdir(parents=True, exist_ok=True)
        # Copy the generated code from the temporary directory to the target directory.
        shutil.copytree(generated_dir, TARGET_DIR)
        print("Successfully generated and copied client code to", TARGET_DIR)


if __name__ == "__main__":
    main()
