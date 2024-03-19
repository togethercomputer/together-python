import base64
import click
import pathlib

from together import Together

from together.types import ImageResponse
from together.types.images import ImageChoicesData


@click.group()
@click.pass_context
def images(ctx: click.Context) -> None:
    """Images generations API commands"""
    pass


@images.command()
@click.pass_context
@click.argument("prompt", type=str, required=True)
@click.option("--model", type=str, required=True, help="Model name")
@click.option("--steps", type=int, default=20, help="Number of steps to run generation")
@click.option("--seed", type=int, default=None, help="Random seed")
@click.option("--n", type=int, default=1, help="Number of images to generate")
@click.option("--height", type=int, default=1024, help="Image height")
@click.option("--width", type=int, default=1024, help="Image width")
@click.option("--negative-prompt", type=str, default=None, help="Negative prompt")
@click.option(
    "--output",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    required=False,
    default=pathlib.Path("."),
    help="Output directory",
)
@click.option("--prefix", type=str, required=False, default="image-")
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    steps: int,
    seed: int,
    n: int,
    height: int,
    width: int,
    negative_prompt: str,
    output: pathlib.Path,
    prefix: str,
) -> None:
    """Generate image"""

    client: Together = ctx.obj

    response = client.images.generate(
        prompt=prompt,
        model=model,
        steps=steps,
        seed=seed,
        n=n,
        height=height,
        width=width,
        negative_prompt=negative_prompt,
    )

    assert isinstance(response, ImageResponse)
    assert isinstance(response.data, list)
    for choice in response.data:
        assert isinstance(choice, ImageChoicesData)

        with open(f"{output}/{prefix}{choice.index}.png", "wb") as f:
            f.write(base64.b64decode(choice.b64_json))
