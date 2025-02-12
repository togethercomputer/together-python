from __future__ import annotations

import sys
from functools import wraps
from typing import Any, Callable, Dict, List, Literal, TypeVar, Union

import click

from together import Together
from together.error import AuthenticationError, InvalidRequestError
from together.generated.exceptions import ForbiddenException, ServiceException
from together.types import DedicatedEndpoint, ListEndpoint


F = TypeVar("F", bound=Callable[..., Any])


def print_endpoint(endpoint: Union[DedicatedEndpoint, ListEndpoint], json: bool = False):
    """Print endpoint details in a Docker-like format or JSON."""
    if json:
        import json as json_lib

        output: Dict[str, Any] = {
            "id": endpoint.id,
            "name": endpoint.name,
            "model": endpoint.model,
            "type": endpoint.type,
            "owner": endpoint.owner,
            "state": endpoint.state,
            "created_at": endpoint.created_at.isoformat(),
        }

        if isinstance(endpoint, DedicatedEndpoint):
            output.update(
                {
                    "display_name": endpoint.display_name,
                    "hardware": endpoint.hardware,
                    "autoscaling": {
                        "min_replicas": endpoint.autoscaling.min_replicas,
                        "max_replicas": endpoint.autoscaling.max_replicas,
                    },
                }
            )

        click.echo(json_lib.dumps(output, indent=2))
        return

    # Print header info
    click.echo(f"ID:\t\t{endpoint.id}")
    click.echo(f"Name:\t\t{endpoint.name}")

    # Print type-specific fields
    if isinstance(endpoint, DedicatedEndpoint):
        click.echo(f"Display Name:\t{endpoint.display_name}")
        click.echo(f"Hardware:\t{endpoint.hardware}")
        click.echo(
            f"Autoscaling:\tMin={endpoint.autoscaling.min_replicas}, "
            f"Max={endpoint.autoscaling.max_replicas}"
        )

    click.echo(f"Model:\t\t{endpoint.model}")
    click.echo(f"Type:\t\t{endpoint.type}")
    click.echo(f"Owner:\t\t{endpoint.owner}")
    click.echo(f"State:\t\t{endpoint.state}")
    click.echo(f"Created:\t{endpoint.created_at}")


def handle_api_errors(f: F) -> F:
    """Decorator to handle common API errors in CLI commands."""

    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return f(*args, **kwargs)
        except (ForbiddenException, ServiceException) as e:
            error_details = ""
            if e.data is not None:
                error_details = e.data.to_dict()["error"]["message"]
            else:
                error_details = str(e)

            if "credentials" in error_details.lower() or "authentication" in error_details.lower():
                click.echo("Error: Invalid API key or authentication failed", err=True)
            else:
                click.echo(f"Error: {error_details}", err=True)
            sys.exit(1)
        except AuthenticationError as e:
            click.echo(f"Error details: {str(e)}", err=True)
            click.echo("Error: Invalid API key or authentication failed", err=True)
            sys.exit(1)
        except InvalidRequestError as e:
            click.echo(f"Error details: {str(e)}", err=True)
            click.echo("Error: Invalid request", err=True)
            sys.exit(1)
        except Exception as e:
            click.echo(f"Error: An unexpected error occurred - {str(e)}", err=True)
            sys.exit(1)

    return wrapper  # type: ignore


@click.group()
@click.pass_context
def endpoints(ctx: click.Context) -> None:
    """Endpoints API commands"""
    pass


@endpoints.command()
@click.option(
    "--model",
    required=True,
    help="The model to deploy (e.g. mistralai/Mixtral-8x7B-Instruct-v0.1)",
)
@click.option(
    "--min-replicas",
    type=int,
    default=1,
    help="Minimum number of replicas to deploy",
)
@click.option(
    "--max-replicas",
    type=int,
    default=1,
    help="Maximum number of replicas to deploy",
)
@click.option(
    "--gpu",
    type=click.Choice(["h100", "a100", "l40", "l40s", "rtx-6000"]),
    required=True,
    help="GPU type to use for inference",
)
@click.option(
    "--gpu-count",
    type=int,
    default=1,
    help="Number of GPUs to use per replica",
)
@click.option(
    "--display-name",
    help="A human-readable name for the endpoint",
)
@click.option(
    "--no-prompt-cache",
    is_flag=True,
    help="Disable the prompt cache for this endpoint",
)
@click.option(
    "--no-speculative-decoding",
    is_flag=True,
    help="Disable speculative decoding for this endpoint",
)
@click.option(
    "--no-auto-start",
    is_flag=True,
    help="Create the endpoint in STOPPED state instead of auto-starting it",
)
@click.pass_obj
@handle_api_errors
def create(
    client: Together,
    model: str,
    min_replicas: int,
    max_replicas: int,
    gpu: str,
    gpu_count: int,
    display_name: str | None,
    no_prompt_cache: bool,
    no_speculative_decoding: bool,
    no_auto_start: bool,
):
    """Create a new dedicated inference endpoint."""
    # Map GPU types to their full hardware ID names
    gpu_map = {
        "h100": "nvidia_h100_80gb_sxm",
        "a100": "nvidia_a100_80gb_pcie" if gpu_count == 1 else "nvidia_a100_80gb_sxm",
        "l40": "nvidia_l40",
        "l40s": "nvidia_l40s",
        "rtx-6000": "nvidia_rtx_6000_ada",
    }

    hardware_id = f"{gpu_count}x_{gpu_map[gpu]}"

    response = client.endpoints.create(
        model=model,
        hardware=hardware_id,
        min_replicas=min_replicas,
        max_replicas=max_replicas,
        display_name=display_name,
        disable_prompt_cache=no_prompt_cache,
        disable_speculative_decoding=no_speculative_decoding,
        state="STOPPED" if no_auto_start else "STARTED",
    )

    # Print detailed information to stderr
    click.echo("Created dedicated endpoint with:", err=True)
    click.echo(f"  Model: {model}", err=True)
    click.echo(f"  Min replicas: {min_replicas}", err=True)
    click.echo(f"  Max replicas: {max_replicas}", err=True)
    click.echo(f"  Hardware: {hardware_id}", err=True)
    if display_name:
        click.echo(f"  Display name: {display_name}", err=True)
    if no_prompt_cache:
        click.echo("  Prompt cache: disabled", err=True)
    if no_speculative_decoding:
        click.echo("  Speculative decoding: disabled", err=True)
    if no_auto_start:
        click.echo("  Auto-start: disabled", err=True)

    click.echo("Endpoint created successfully, id: ", err=True)
    # Print only the endpoint ID to stdout
    click.echo(response.id)


@endpoints.command()
@click.argument("endpoint-id", required=True)
@click.option("--json", is_flag=True, help="Print output in JSON format")
@click.pass_obj
@handle_api_errors
def get(client: Together, endpoint_id: str, json: bool):
    """Get a dedicated inference endpoint."""
    endpoint = client.endpoints.get(endpoint_id)
    print_endpoint(endpoint, json=json)


@endpoints.command()
@click.argument("endpoint-id", required=True)
@click.pass_obj
@handle_api_errors
def stop(client: Together, endpoint_id: str):
    """Stop a dedicated inference endpoint."""
    client.endpoints.update(endpoint_id, state="STOPPED")
    click.echo("Successfully stopped endpoint", err=True)
    click.echo(endpoint_id)


@endpoints.command()
@click.argument("endpoint-id", required=True)
@click.pass_obj
@handle_api_errors
def start(client: Together, endpoint_id: str):
    """Start a dedicated inference endpoint."""
    client.endpoints.update(endpoint_id, state="STARTED")
    click.echo("Successfully started endpoint", err=True)
    click.echo(endpoint_id)


@endpoints.command()
@click.argument("endpoint-id", required=True)
@click.pass_obj
@handle_api_errors
def delete(client: Together, endpoint_id: str):
    """Delete a dedicated inference endpoint."""
    client.endpoints.delete(endpoint_id)
    click.echo("Successfully deleted endpoint", err=True)
    click.echo(endpoint_id)


@endpoints.command()
@click.option("--json", is_flag=True, help="Print output in JSON format")
@click.option(
    "--type", type=click.Choice(["dedicated", "serverless"]), help="Filter by endpoint type"
)
@click.pass_obj
@handle_api_errors
def list(client: Together, json: bool, type: Literal["dedicated", "serverless"] | None) -> None:
    """List all inference endpoints (includes both dedicated and serverless endpoints)."""
    endpoints: List[ListEndpoint] = client.endpoints.list(type=type)

    if not endpoints:
        click.echo("No dedicated endpoints found", err=True)
        return

    click.echo("Dedicated endpoints:", err=True)
    for endpoint in endpoints:
        print_endpoint(endpoint, json=json)
        click.echo()


@endpoints.command()
@click.argument("endpoint-id", required=True)
@click.option(
    "--display-name",
    help="A new human-readable name for the endpoint",
)
@click.option(
    "--min-replicas",
    type=int,
    help="New minimum number of replicas to maintain",
)
@click.option(
    "--max-replicas",
    type=int,
    help="New maximum number of replicas to scale up to",
)
@click.pass_obj
@handle_api_errors
def update(
    client: Together,
    endpoint_id: str,
    display_name: str | None,
    min_replicas: int | None,
    max_replicas: int | None,
):
    """Update a dedicated inference endpoint's configuration."""
    if not any([display_name, min_replicas, max_replicas]):
        click.echo("Error: At least one update option must be specified", err=True)
        sys.exit(1)

    # If only one of min/max replicas is specified, we need both for the update
    if (min_replicas is None) != (max_replicas is None):
        click.echo(
            "Error: Both --min-replicas and --max-replicas must be specified together",
            err=True,
        )
        sys.exit(1)

    # Build kwargs for the update
    kwargs = {}
    if display_name is not None:
        kwargs["display_name"] = display_name
    if min_replicas is not None and max_replicas is not None:
        kwargs["min_replicas"] = min_replicas
        kwargs["max_replicas"] = max_replicas

    _response = client.endpoints.update(endpoint_id, **kwargs)

    # Print what was updated
    click.echo("Updated endpoint configuration:", err=True)
    if display_name:
        click.echo(f"  Display name: {display_name}", err=True)
    if min_replicas is not None and max_replicas is not None:
        click.echo(f"  Min replicas: {min_replicas}", err=True)
        click.echo(f"  Max replicas: {max_replicas}", err=True)

    click.echo("Successfully updated endpoint", err=True)
    click.echo(endpoint_id)
