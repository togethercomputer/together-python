import click
import json

from tabulate import tabulate

from together import Together
from together.utils import parse_timestamp, finetune_price_to_dollars


@click.group(name="fine-tune")
@click.pass_context
def fine_tune(ctx: click.Context) -> None:
    """Convert utilities."""
    pass


@fine_tune.command()
@click.pass_context
@click.option("--training_file", type=str, required=True)
@click.option("--model", type=str, required=True)
@click.option("--n-epochs", type=int, default=1)
@click.option("--n-checkpoints", type=int, default=1)
@click.option("--batch-size", type=int, default=32)
@click.option("--learning-rate", type=float, default=3e-5)
@click.option("--suffix", type=str, default=None)
@click.option("--wandb-api-key", prompt=True, hide_input=True)
def create(
    ctx: click.Context,
    training_file: str,
    model: str,
    n_epochs: int,
    n_checkpoints: int,
    batch_size: int,
    learning_rate: float,
    suffix: str,
    wandb_api_key: str,
) -> None:
    """Start fine-tuning"""
    client: Together = ctx.obj

    response = client.fine_tuning.create(
        training_file=training_file,
        model=model,
        n_epochs=n_epochs,
        n_checkpoints=n_checkpoints,
        batch_size=batch_size,
        learning_rate=learning_rate,
        suffix=suffix,
        wandb_api_key=wandb_api_key,
    )

    click.echo(json.dumps(response.model_dump(), indent=4))


@fine_tune.command()
@click.pass_context
def list(ctx: click.Context) -> None:
    """List fine-tuning tasks"""
    client: Together = ctx.obj

    response = client.fine_tuning.list()

    assert response.data

    response.data.sort(key=lambda x: parse_timestamp(x.created_at or ""))

    display_list = []
    for i in response.data:
        display_list.append(
            {
                "Fine-tune ID": i.id,
                "Model Output Name": i.output_name,
                "Status": i.status,
                "Created At": i.created_at,
                "Price": finetune_price_to_dollars(
                    float(str(i.total_price))
                ),  # convert to string for mypy typing
            }
        )
    table = tabulate(display_list, headers="keys", tablefmt="grid", showindex=True)

    click.echo(table)


@fine_tune.command()
@click.pass_context
@click.argument("fine_tune_id", type=str, required=True)
def retrieve(ctx: click.Context, fine_tune_id: str) -> None:
    """Retrieve fine-tuning task"""
    client: Together = ctx.obj

    response = client.fine_tuning.retrieve(fine_tune_id)

    table_data = [
        {"Key": key, "Value": value}
        for key, value in response.model_dump().items()
        if key not in ["events"]
    ]
    table = tabulate(table_data, tablefmt="grid")

    click.echo(table)


@fine_tune.command()
@click.pass_context
@click.argument("fine_tune_id", type=str, required=True)
def cancel(ctx: click.Context, fine_tune_id: str) -> None:
    """Cancel fine-tuning task"""
    client: Together = ctx.obj

    response = client.fine_tuning.cancel(fine_tune_id)

    click.echo(json.dumps(response.model_dump(), indent=4))


@fine_tune.command()
@click.pass_context
@click.argument("fine_tune_id", type=str, required=True)
def list_events(ctx: click.Context, fine_tune_id: str) -> None:
    """List fine-tuning events"""
    client: Together = ctx.obj

    response = client.fine_tuning.list_events(fine_tune_id)

    assert response.data

    display_list = []
    for i in response.data:
        display_list.append(
            {
                "Message": i.message,
                "Type": i.type,
                "Created At": parse_timestamp(i.created_at or ""),
                "Hash": i.hash,
            }
        )
    table = tabulate(display_list, headers="keys", tablefmt="grid", showindex=True)

    click.echo(table)


@fine_tune.command()
@click.pass_context
@click.argument("fine_tune_id", type=str, required=True)
@click.option(
    "--output_dir",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    required=False,
    default=".",
)
@click.option("--checkpoint-step", type=int, required=False, default=-1)
def download(
    ctx: click.Context, fine_tune_id: str, output_dir: str, checkpoint_step: int
) -> None:
    """Download fine-tuning checkpoint"""
    client: Together = ctx.obj

    response = client.fine_tuning.download(
        fine_tune_id, output=output_dir, checkpoint_step=checkpoint_step
    )

    click.echo(json.dumps(response.model_dump(), indent=4))
