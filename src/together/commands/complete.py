from __future__ import annotations

import argparse
import json
import re
import typing
from typing import List

import together
from together import Complete
from together.error import ResponseError
from together.tools.types import Choice, TogetherResponse


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    COMMAND_NAME = "complete"
    subparser = subparsers.add_parser(COMMAND_NAME)

    subparser.add_argument(
        "prompt",
        metavar="PROMPT",
        default=None,
        type=str,
        help="A string providing context for the model to complete.",
    )

    subparser.add_argument(
        "--model",
        "-m",
        default=together.default_text_model,
        type=str,
        help=f"The name of the model to query. Default={together.default_text_model}",
    )

    subparser.add_argument(
        "--no-stream",
        default=False,
        action="store_true",
        help="Indicates wether to disable streaming",
    )

    subparser.add_argument(
        "--max-tokens",
        default=128,
        type=int,
        help="Maximum number of tokens to generate. Default=128",
    )
    subparser.add_argument(
        "--stop",
        default=["<human>"],
        nargs="+",
        type=str,
        metavar="STOP_WORD",
        help="Strings that will truncate (stop) text generation. Default='<human>'",
    )
    subparser.add_argument(
        "--temperature",
        default=0.7,
        type=float,
        help="Determines the degree of randomness in the response. Default=0.7",
    )
    subparser.add_argument(
        "--top-p",
        default=0.7,
        type=float,
        help="Used to dynamically adjust the number of choices for each predicted token based on the cumulative probabilities. Default=0.7",
    )
    subparser.add_argument(
        "--top-k",
        default=50,
        type=int,
        help="Used to limit the number of choices for the next predicted word or token. Default=50",
    )
    subparser.add_argument(
        "--repetition-penalty",
        default=None,
        type=float,
        help="Controls the diversity of generated text by reducing the likelihood of repeated sequences. Higher values decrease repetition.",
    )
    subparser.add_argument(
        "--seed",
        default=None,
        type=int,
        help="Specifies generation seed",
    )
    subparser.add_argument(
        "--details",
        default=False,
        action="store_true",
        help="Return details with generation",
    )
    subparser.add_argument(
        "--raw",
        default=False,
        action="store_true",
        help="Return raw response from API",
    )
    subparser.set_defaults(func=_run_complete)


def _enforce_stop_tokens(text: str, stop: List[str]) -> str:
    """Cut off the text as soon as any stop words occur."""
    return re.split("|".join(stop), text)[0]


def no_streamer(args: argparse.Namespace, response: TogetherResponse) -> None:
    if args.raw:
        print(json.dumps(response.model_dump(), indent=4))

    else:
        if response.choices:
            text = str(response.choices[0].text)
            print(text.strip())
        elif response.error:
            raise ResponseError(response.error)
        else:
            raise ResponseError(
                f"Unknown error occured. Received unhandled response: {response}"
            )


def _run_complete(args: argparse.Namespace) -> None:
    if args.no_stream:
        response = Complete.create(
            prompt=args.prompt,
            model=args.model,
            max_tokens=args.max_tokens,
            stop=args.stop,
            temperature=args.temperature,
            top_p=args.top_p,
            top_k=args.top_k,
            repetition_penalty=args.repetition_penalty,
            details=args.details,
            seed=args.seed,
            stream=False,
        )

        no_streamer(args, typing.cast(TogetherResponse, response))
    else:
        for token in Complete.create(
            prompt=args.prompt,
            model=args.model,
            max_tokens=args.max_tokens,
            stop=args.stop,
            temperature=args.temperature,
            top_p=args.top_p,
            top_k=args.top_k,
            repetition_penalty=args.repetition_penalty,
            details=args.details,
            seed=args.seed,
            stream=True,
            raw=args.raw,
        ):
            token = typing.cast(TogetherResponse, token)
            choices = typing.cast(List[Choice], token.choices)
            if not args.raw:
                print(choices[0].text, end="", flush=True)
            else:
                print(token)
        if not args.raw:
            print("\n")
