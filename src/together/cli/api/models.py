import json as json_lib

import click
from tabulate import tabulate

from together import Together
from together.types.models import ModelObject


@click.group()
@click.pass_context
def models(ctx: click.Context) -> None:
    """Models API commands"""
    pass


@models.command()
@click.option(
    "--type",
    type=click.Choice(["dedicated"]),
    help="Filter models by type (dedicated: models that can be deployed as dedicated endpoints)",
)
@click.option(
    "--json",
    is_flag=True,
    help="Output in JSON format",
)
@click.pass_context
def list(ctx: click.Context, type: str | None, json: bool) -> None:
    """List models"""
    client: Together = ctx.obj

    response = client.models.list(dedicated=(type == "dedicated"))

    display_list = []

    model: ModelObject
    for model in response:
        display_list.append(
            {
                "ID": model.id,
                "Name": model.display_name,
                "Organization": model.organization,
                "Type": model.type,
                "Context Length": model.context_length,
                "License": model.license,
                "Input per 1M token": model.pricing.input,
                "Output per 1M token": model.pricing.output,
            }
        )

    if json:
        click.echo(json_lib.dumps(display_list, indent=2))
    else:
        click.echo(tabulate(display_list, headers="keys", tablefmt="plain"))
