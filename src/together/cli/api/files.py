import click
import json
import pathlib

from together import Together
from together.types import FilePurpose


@click.group()
@click.pass_context
def files(ctx: click.Context) -> None:
    """Convert utilities."""
    pass


@files.command()
@click.pass_context
@click.argument(
    "file",
    type=click.Path(
        exists=True, file_okay=True, resolve_path=True, readable=True, dir_okay=False
    ),
    required=True,
)
@click.option(
    "--purpose",
    type=str,
    default=FilePurpose.FineTune.value,
    help="Purpose of file upload. Acceptable values in enum `together.types.FilePurpose`. Defaults to `fine-tunes`.",
)
def upload(ctx: click.Context, file: pathlib.Path, purpose: str) -> None:
    """Upload file"""

    client: Together = ctx.obj

    response = client.files.upload(file=file, purpose=purpose)

    click.echo(json.dumps(response.model_dump(), indent=4))


@files.command()
@click.pass_context
def list(ctx: click.Context) -> None:
    """List files"""
    client: Together = ctx.obj

    response = client.files.list()

    click.echo(json.dumps(response.model_dump(), indent=4))


@files.command()
@click.pass_context
@click.argument("id", type=str, required=True)
def retrieve(ctx: click.Context, id: str) -> None:
    """Upload file"""

    client: Together = ctx.obj

    response = client.files.retrieve(id=id)

    click.echo(json.dumps(response.model_dump(), indent=4))


@files.command()
@click.pass_context
@click.argument("id", type=str, required=True)
@click.option("--output", type=str, default=None, help="Output filename")
def retrieve_content(ctx: click.Context, id: str, output: str) -> None:
    """Retrieve file content and output to file"""

    client: Together = ctx.obj

    response = client.files.retrieve_content(id=id, output=output)

    click.echo(json.dumps(response.model_dump(), indent=4))


@files.command()
@click.pass_context
@click.argument("id", type=str, required=True)
def delete(ctx: click.Context, id: str) -> None:
    """Delete remote file"""

    client: Together = ctx.obj

    response = client.files.delete(id=id)

    click.echo(json.dumps(response.model_dump(), indent=4))
