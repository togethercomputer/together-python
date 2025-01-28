from __future__ import annotations

import click


@click.group()
def inference():
    """Manage inference endpoints and configurations."""
    pass


@inference.group()
def dedicated():
    """Manage dedicated inference endpoints."""
    pass


@dedicated.command()
@click.pass_obj
def create(client):
    """Create a new dedicated inference endpoint."""
    click.echo("Creating new dedicated inference endpoint...")
    # TODO: Implement the actual endpoint creation logic
    pass
