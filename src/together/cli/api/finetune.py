import json
from textwrap import wrap

import click
from tabulate import tabulate

from together import Together
from together.utils import finetune_price_to_dollars, parse_timestamp


@click.group(name="fine-tuning")
@click.pass_context
def fine_tuning(ctx: click.Context) -> None:
    """Fine-tunes API commands"""
    pass


@fine_tuning.command()
@click.pass_context
@click.option(
    "--training-file", type=str, required=True, help="Training file ID from Files API"
)
@click.option("--model", type=str, required=True, help="Base model name")
@click.option("--n-epochs", type=int, default=1, help="Number of epochs to train for")
@click.option(
    "--n-checkpoints", type=int, default=1, help="Number of checkpoints to save"
)
@click.option("--batch-size", type=int, default=32, help="Train batch size")
@click.option("--learning-rate", type=float, default=3e-5, help="Learning rate")
@click.option(
    "--suffix", type=str, default=None, help="Suffix for the fine-tuned model name"
)
@click.option("--wandb-api-key", type=str, default=None, help="Wandb API key")
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


@fine_tuning.command()
@click.pass_context
def list(ctx: click.Context) -> None:
    """List fine-tuning jobs"""
    client: Together = ctx.obj

    response = client.fine_tuning.list()

    response.data = response.data or []

    response.data.sort(key=lambda x: parse_timestamp(x.created_at or ""))

    display_list = []
    for i in response.data:
        display_list.append(
            {
                "Fine-tune ID": i.id,
                "Model Output Name": "\n".join(wrap(i.output_name or "", width=30)),
                "Status": i.status,
                "Created At": i.created_at,
                "Price": f"""${finetune_price_to_dollars(
                    float(str(i.total_price))
                )}""",  # convert to string for mypy typing
            }
        )
    table = tabulate(display_list, headers="keys", tablefmt="grid", showindex=True)

    click.echo(table)


@fine_tuning.command()
@click.pass_context
@click.argument("fine_tune_id", type=str, required=True)
def retrieve(ctx: click.Context, fine_tune_id: str) -> None:
    """Retrieve fine-tuning job details"""
    client: Together = ctx.obj

    response = client.fine_tuning.retrieve(fine_tune_id)

    # remove events from response for cleaner output
    response.events = None

    click.echo(json.dumps(response.model_dump(), indent=4))


@fine_tuning.command()
@click.pass_context
@click.argument("fine_tune_id", type=str, required=True)
@click.option(
    "--quiet", is_flag=True, help="Do not prompt for confirmation before cancelling job"
)
def cancel(ctx: click.Context, fine_tune_id: str, quiet: bool = False) -> None:
    """Cancel fine-tuning job"""
    client: Together = ctx.obj
    if not quiet:
        confirm_response = input(
            "You will be billed for any completed training steps upon cancellation. "
            f"Do you want to cancel job {fine_tune_id}? [y/N]"
        )
        if "y" not in confirm_response.lower():
            click.echo({"status": "Cancel not submitted"})
            return
    response = client.fine_tuning.cancel(fine_tune_id)

    click.echo(json.dumps(response.model_dump(), indent=4))


@fine_tuning.command()
@click.pass_context
@click.argument("fine_tune_id", type=str, required=True)
def list_events(ctx: click.Context, fine_tune_id: str) -> None:
    """List fine-tuning events"""
    client: Together = ctx.obj

    response = client.fine_tuning.list_events(fine_tune_id)

    response.data = response.data or []

    display_list = []
    for i in response.data:
        display_list.append(
            {
                "Message": "\n".join(wrap(i.message or "", width=50)),
                "Type": i.type,
                "Created At": parse_timestamp(i.created_at or ""),
                "Hash": i.hash,
            }
        )
    table = tabulate(display_list, headers="keys", tablefmt="grid", showindex=True)

    click.echo(table)


@fine_tuning.command()
@click.pass_context
@click.argument("fine_tune_id", type=str, required=True)
@click.option(
    "--output_dir",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    required=False,
    default=None,
    help="Output directory",
)
@click.option(
    "--checkpoint-step",
    type=int,
    required=False,
    default=-1,
    help="Download fine-tuning checkpoint. Defaults to latest.",
)
def download(
    ctx: click.Context,
    fine_tune_id: str,
    output_dir: str,
    checkpoint_step: int,
) -> None:
    """Download fine-tuning checkpoint"""
    client: Together = ctx.obj

    response = client.fine_tuning.download(
        fine_tune_id, output=output_dir, checkpoint_step=checkpoint_step
    )

    click.echo(json.dumps(response.model_dump(), indent=4))
