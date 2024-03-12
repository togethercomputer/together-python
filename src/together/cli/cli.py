import click
import os

import together
from together.constants import TIMEOUT_SECS, MAX_RETRIES

from together.cli.api.files import files
from together.cli.api.completions import completions


@click.group()
@click.pass_context
@click.option(
    "--api-key",
    type=str,
    help="API Key. Defaults to environment variable `TOGETHER_API_KEY`",
    default=os.getenv("TOGETHER_API_KEY"),
)
@click.option(
    "--base-url", type=str, help="API Base URL. Defaults to Together AI endpoint."
)
@click.option(
    "--timeout", type=int, help=f"Request timeout. Defaults to {TIMEOUT_SECS} seconds"
)
@click.option(
    "--max-retries",
    type=int,
    help=f"Maximum number of HTTP retries. Defaults to {MAX_RETRIES}.",
)
@click.option("--debug", help="Debug mode", is_flag=True)
def main(
    ctx: click.Context,
    api_key: str | None,
    base_url: str | None,
    timeout: int | None,
    max_retries: int | None,
    debug: bool | None,
) -> None:
    """This is a sample CLI tool."""
    together.log = "debug" if debug else None
    ctx.obj = together.Together(
        api_key=api_key, base_url=base_url, timeout=timeout, max_retries=max_retries
    )


main.add_command(completions)
main.add_command(files)

if __name__ == "__main__":
    main()
