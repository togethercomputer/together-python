import click
import json

from together import Together
from together.types import CompletionChunk
from together.types.completions import CompletionResponse, CompletionChoicesChunk
from typing import List


@click.command()
@click.pass_context
@click.argument("prompt", type=str, required=True)
@click.option("--model", type=str, required=True)
@click.option("--no-stream", is_flag=True)
@click.option("--max-tokens", type=int)
@click.option("--stop", type=str, multiple=True)
@click.option("--temperature", type=float)
@click.option("--top-p", type=int)
@click.option("--top-k", type=float)
@click.option("--logprobs", type=int)
@click.option("--echo", is_flag=True)
@click.option("--n", type=int)
@click.option("--safety-model", type=str)
@click.option("--raw", is_flag=True)
def completions(
    ctx: click.Context,
    prompt: str,
    model: str,
    max_tokens: int | None = 512,
    stop: List[str] | None = None,
    temperature: float | None = None,
    top_p: float | None = None,
    top_k: int | None = None,
    repetition_penalty: float | None = None,
    no_stream: bool = False,
    logprobs: int | None = None,
    echo: bool | None = None,
    n: int | None = None,
    safety_model: str | None = None,
    raw: bool = False,
) -> None:
    """Convert utilities."""
    client: Together = ctx.obj

    response = client.completions.create(
        model=model,
        prompt=prompt,
        top_p=top_p,
        top_k=top_k,
        temperature=temperature,
        max_tokens=max_tokens,
        stop=stop,
        repetition_penalty=repetition_penalty,
        stream=not no_stream,
        logprobs=logprobs,
        echo=echo,
        n=n,
        safety_model=safety_model,
    )

    if not no_stream:
        for chunk in response:
            # assertions for type checking
            assert isinstance(chunk, CompletionChunk)
            assert chunk.choices

            if raw:
                click.echo(f"{json.dumps(chunk.model_dump())}")
                continue

            should_print_header = len(chunk.choices) > 1
            for stream_choice in sorted(chunk.choices, key=lambda c: c.index):  # type: ignore
                # assertions for type checking
                assert isinstance(stream_choice, CompletionChoicesChunk)
                assert stream_choice.delta
                assert stream_choice.delta.content

                if should_print_header:
                    click.echo(f"\n===== Completion {stream_choice.index} =====\n")
                click.echo(f"{stream_choice.delta.content}", nl=False)

                if should_print_header:
                    click.echo("\n")

        # new line after stream ends
        click.echo("\n")
    else:
        # assertions for type checking
        assert isinstance(response, CompletionResponse)
        assert isinstance(response.choices, list)

        if raw:
            click.echo(f"{json.dumps(response.model_dump(), indent=4)}")
            return

        should_print_header = len(response.choices) > 1
        for i, choice in enumerate(response.choices):
            if should_print_header:
                click.echo(f"===== Completion {i} =====")
            click.echo(choice.text)

            if should_print_header or not choice.text.endswith("\n"):
                click.echo("\n")
