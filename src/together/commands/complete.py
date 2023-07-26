from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from typing import Any, Dict, List

import together
from together import Complete, get_logger


def add_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
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
        "--logprobs",
        default=None,
        type=int,
        help="Specifies how many top token log probabilities are included in the response for each token generation step.",
    )
    subparser.add_argument(
        "--raw",
        default=False,
        action="store_true",
        help="temperature for the LM",
    )
    subparser.set_defaults(func=_run_complete)


def _enforce_stop_tokens(text: str, stop: List[str]) -> str:
    """Cut off the text as soon as any stop words occur."""
    return re.split("|".join(stop), text)[0]


def no_streamer(
    args: argparse.Namespace, response: Dict[str, Any], logger: logging.Logger
) -> None:
    if args.raw:
        print(json.dumps(response, indent=4))
        sys.exit()

    if "output" in response.keys():
        try:
            text = str(response["output"]["choices"][0]["text"])
        except Exception:
            try:
                logger.critical(f"Error raised: {response['output']['error']}")
                raise together.ResponseError(response["output"]["error"])
            except Exception as e:
                logger.critical(f"Error raised: {e}")
                raise together.ResponseError(e)

        # if args.stop is not None:
        #    text = _enforce_stop_tokens(text, args.stop)

    elif "error" in response.keys():
        if response["error"] == "Returned error: no instance":
            logger.critical(
                f"No running instances for {args.model}. You can start an instance by navigating to the Together Playground at api.together.xyz"
            )
            raise together.InstanceError(model=args.model)
        else:
            logger.critical(f"Error raised: {response['error']}")

    else:
        logger.critical("Unknown response received")
        raise together.ResponseError("Unknown response received. Please try again.")

    print(text.strip())


def _run_complete(args: argparse.Namespace) -> None:
    logger = get_logger(__name__, log_level=args.log)

    complete = Complete()

    if args.no_stream:
        response = complete.create(
            prompt=args.prompt,
            model=args.model,
            max_tokens=args.max_tokens,
            stop=args.stop,
            temperature=args.temperature,
            top_p=args.top_p,
            top_k=args.top_k,
            repetition_penalty=args.repetition_penalty,
            logprobs=args.logprobs,
        )
        no_streamer(args, response, logger)
    else:
        for text in complete.create_streaming(
            prompt=args.prompt,
            model=args.model,
            max_tokens=args.max_tokens,
            stop=args.stop,
            temperature=args.temperature,
            top_p=args.top_p,
            top_k=args.top_k,
            repetition_penalty=args.repetition_penalty,
        ):
            print(text, end="", flush=True)
        print("\n")
