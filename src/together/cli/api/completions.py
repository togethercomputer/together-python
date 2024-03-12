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
@click.option("--stream", is_flag=True)
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
    stream: bool = False,
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
        stream=stream,
        logprobs=logprobs,
        echo=echo,
        n=n,
        safety_model=safety_model,
    )

    if stream:
        for chunk in response:
            assert isinstance(chunk, CompletionChunk)
            assert isinstance(chunk.choices, list)
            should_print_header = len(chunk.choices) > 1
            for stream_choice in sorted(chunk.choices, key=lambda c: c.index):  # type: ignore
                assert isinstance(stream_choice, CompletionChoicesChunk)
                if raw:
                    click.echo(f"{json.dumps(stream_choice.model_dump())}\n")
                    continue

                if should_print_header:
                    click.echo(f"===== Completion {stream_choice.index} =====\n")
                click.echo(f"{stream_choice.delta}")

                if should_print_header:
                    click.echo("\n")
    else:
        assert isinstance(response, CompletionResponse)
        assert isinstance(response.choices, list)
        should_print_header = len(response.choices) > 1
        for i, choice in enumerate(response.choices):
            if raw:
                click.echo(f"{json.dumps(choice.model_dump())}\n")
                continue

            if should_print_header:
                click.echo(f"===== Completion {i} =====\n")
            click.echo(choice.text)

            if should_print_header or not choice.text.endswith("\n"):
                click.echo("\n")
