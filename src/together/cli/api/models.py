import json as json_lib

import click
from tabulate import tabulate

from together import Together
from together.types.models import ModelObject, ModelUploadResponse


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


@models.command()
@click.option(
    "--model-name",
    required=True,
    help="The name to give to your uploaded model",
)
@click.option(
    "--model-source",
    required=True,
    help="The source location of the model (Hugging Face repo or S3 path)",
)
@click.option(
    "--model-type",
    type=click.Choice(["model", "adapter"]),
    default="model",
    help="Whether the model is a full model or an adapter",
)
@click.option(
    "--hf-token",
    help="Hugging Face token (if uploading from Hugging Face)",
)
@click.option(
    "--description",
    help="A description of your model",
)
@click.option(
    "--base-model",
    help="The base model to use for an adapter if setting it to run against a serverless pool. Only used for model_type 'adapter'.",
)
@click.option(
    "--lora-model",
    help="The lora pool to use for an adapter if setting it to run against, say, a dedicated pool. Only used for model_type 'adapter'.",
)
@click.option(
    "--json",
    is_flag=True,
    help="Output in JSON format",
)
@click.pass_context
def upload(
    ctx: click.Context,
    model_name: str,
    model_source: str,
    model_type: str,
    hf_token: str | None,
    description: str | None,
    base_model: str | None,
    lora_model: str | None,
    json: bool,
) -> None:
    """Upload a custom model or adapter from Hugging Face or S3"""
    client: Together = ctx.obj

    response: ModelUploadResponse = client.models.upload(
        model_name=model_name,
        model_source=model_source,
        model_type=model_type,
        hf_token=hf_token,
        description=description,
        base_model=base_model,
        lora_model=lora_model,
    )

    if json:
        click.echo(json_lib.dumps(response.model_dump(), indent=2))
    else:
        click.echo(f"Model upload job created successfully!")
        if response.job_id:
            click.echo(f"Job ID: {response.job_id}")
        if response.model_name:
            click.echo(f"Model Name: {response.model_name}")
        if response.model_id:
            click.echo(f"Model ID: {response.model_id}")
        if response.model_source:
            click.echo(f"Model Source: {response.model_source}")
        click.echo(f"Message: {response.message}")
